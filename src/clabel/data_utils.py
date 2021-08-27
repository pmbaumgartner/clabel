import pandas as pd
from typing import NamedTuple, Union, Dict, Tuple, List
from rich.table import Table


def current_cluster_names(cluster_names: Dict[int, str]) -> List[str]:
    return list(sorted(cluster_names.values()))


def get_sorted_cluster_ids(df: pd.DataFrame, cluster_column: str) -> List[str]:
    return sorted(
        df[cluster_column].astype(str).unique(),
        key=lambda d: str(d).zfill(5),
    )


def cluster_counts(df: pd.DataFrame, cluster_column: str) -> pd.DataFrame:
    counts = df[cluster_column].value_counts().rename("Count")
    pcts = df[cluster_column].value_counts(normalize=True).rename("Pct")
    pcts_cumulative = pcts.cumsum().rename("Cumulative Pct")
    result = (
        pd.concat(
            (
                counts,
                pcts,
                pcts_cumulative,
            ),
            axis=1,
        )
        .reset_index()
        .rename(columns={"index": "Cluster ID"})
    )
    return result


def build_summary_df(
    df: pd.DataFrame, cluster_column: str, cluster_names: Dict[int, str]
) -> pd.DataFrame:
    summary_df = cluster_counts(df, cluster_column)
    summary_df["Label"] = summary_df["Cluster ID"].map(cluster_names).fillna("")
    return summary_df


def table_str_fmt(n: Union[float, int]) -> str:
    return f"{n*100:.1f}" if isinstance(n, float) else str(n)


class LabelingSummaryStats(NamedTuple):
    cluster_count_labeled: int
    cluster_pct_labeled: float
    examples_count_labeled: int
    examples_pct_labeled: float

    def strfmt(self, attr: str) -> str:
        n = getattr(self, attr)
        return table_str_fmt(n)


def get_labeling_summary_stats(summary_df: pd.DataFrame) -> LabelingSummaryStats:
    labeled_summary_df = summary_df.query("Label != ''")
    summary_stats = labeled_summary_df[["Pct", "Count"]].sum()
    cluster_count_labeled = len(labeled_summary_df)
    cluster_pct_labeled = cluster_count_labeled / len(summary_df)
    examples_count_labeled = int(summary_stats["Count"])
    examples_pct_labeled = summary_stats["Pct"]
    return LabelingSummaryStats(
        cluster_count_labeled,
        cluster_pct_labeled,
        examples_count_labeled,
        examples_pct_labeled,
    )


def build_rich_cluster_summary_table(summary_df: pd.DataFrame) -> Table:
    cluster_table = Table(title="Cluster Label Summary")
    for column in summary_df.columns:
        cluster_table.add_column(column)
    for row in summary_df.itertuples():
        cluster_table.add_row(*[table_str_fmt(i) for i in row[1:]])
    return cluster_table


def build_rich_stats_table(summary_stats: LabelingSummaryStats) -> Table:
    summary_table = Table(title="Overall Labeling Statistics")
    summary_table.add_column("Element")
    summary_table.add_column("Count")
    summary_table.add_column("Percent")
    summary_table.add_row(
        "Clusters",
        summary_stats.strfmt("cluster_count_labeled"),
        summary_stats.strfmt("cluster_pct_labeled"),
    )
    summary_table.add_row(
        "Rows",
        summary_stats.strfmt("examples_count_labeled"),
        summary_stats.strfmt("examples_pct_labeled"),
    )
    return summary_table


def overview(
    df: pd.DataFrame, cluster_column: str, cluster_names: Dict[int, str]
) -> Tuple[Table, Table]:
    summary_df = build_summary_df(df, cluster_column, cluster_names)
    summary_stats = get_labeling_summary_stats(summary_df)
    cluster_table = build_rich_cluster_summary_table(summary_df)
    summary_table = build_rich_stats_table(summary_stats)
    return (cluster_table, summary_table)
