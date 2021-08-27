from time import time
from typing import List

import pandas as pd
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from clabel.data_utils import current_cluster_names, get_sorted_cluster_ids, overview
from clabel.demo import demo_df
from clabel.io import export_summary, get_column_info, import_summary
from clabel.questions import (
    cluster_menu_q,
    cluster_select_q,
    data_location_q,
    data_source_q,
    declare_name_q,
    existing_labels_path_q,
    existing_labels_q,
    export_path_q,
    main_menu_q,
)
from clabel.styles import RICH_THEME


def main():
    console = Console(theme=RICH_THEME)

    console.print("[emphasis]Welcome to CLABEL! The cluster labeling tool.[/]")
    data_source: str = data_source_q.ask()

    DEMO_MODE: bool = data_source == "Demo Mode"
    data_location: str = data_location_q.skip_if(DEMO_MODE).ask()

    with console.status("[emphasis]Reading DataFrame...") as status:
        start = time()
        df = demo_df if DEMO_MODE else pd.read_csv(data_location)
        finish = time()
    console.print(f"[emphasis]DataFrame Loaded in {finish - start:.1f}s")

    existing_labels: bool = existing_labels_q.skip_if(DEMO_MODE).ask()
    if existing_labels:
        existing_labels_path: str = existing_labels_path_q.skip_if(DEMO_MODE).ask()
        cluster_names, text_column, cluster_column = import_summary(
            existing_labels_path
        )
    else:
        text_column, cluster_column = (
            ("texts", "clusters") if DEMO_MODE else get_column_info(df)
        )
        cluster_names = {}

    sorted_cluster_ids = get_sorted_cluster_ids(df, cluster_column)

    main_loop = True
    while main_loop:
        cluster_table, summary_table = overview(df, cluster_column, cluster_names)
        console.print(summary_table)
        console.print(cluster_table)
        menu: str = main_menu_q.ask()
        if menu == "Review Cluster":
            cluster: str = cluster_select_q(sorted_cluster_ids).ask()
            cluster_df = df.query(f"{cluster_column} == {cluster}")
            cluster_size: int = len(cluster_df)
            console.print(
                f"Cluster [emphasis]{cluster}[/] (n={cluster_size}) selected."
            )
            if int(cluster) in cluster_names:
                console.print(
                    f"Cluster [emphasis]{cluster}[/] already labeled with [emphasis]{cluster_names[int(cluster)]}[/]"
                )
                console.print(
                    "[warning]A new cluster Name will overwrite the existing one.[/]"
                )
            cluster_loop = True
            while cluster_loop:
                cluster_menu: str = cluster_menu_q.ask()
                if cluster_menu == "View Cluster Examples":
                    with console.pager():
                        console.rule(f"Cluster {cluster} Examples")
                        console.print(
                            "Being viewed in a PAGER. Press [kb]\[h][/] for help, [kb]\[q][/] to quit.",
                            justify="center",
                        )
                        console.print(
                            Group(*[Panel(text) for text in df["texts"].tolist()])
                        )
                elif cluster_menu == "Declare Name":
                    current_names = current_cluster_names(cluster_names)
                    cluster_name = declare_name_q(current_names).ask()
                    cluster_names[int(cluster)] = cluster_name
                    cluster_loop = False
                else:
                    cluster_loop = False
        elif menu == "Export Cluster Labels & Exit":
            export_path: str = export_path_q.ask()
            export_summary(cluster_names, text_column, cluster_column, export_path)
            console.print(f"Labels exported to [emphasis]{export_path}.")
            console.print("You can load them in next time you label this dataset.")
            main_loop = False
        else:
            main_loop = False


if __name__ == "__main__":
    main()
