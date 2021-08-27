import questionary
from typing import List
from clabel.styles import QUESTIONARY_THEME

data_source_q = questionary.select(
    "Please Select an Option:",
    choices=["Load Data", "Demo Mode"],
    style=QUESTIONARY_THEME,
)

data_location_q = questionary.path(
    "File (.csv): ",
    file_filter=lambda x: x.endswith(".csv"),
    style=QUESTIONARY_THEME,
)

existing_labels_q = questionary.confirm(
    "Do you have existing labels?", style=QUESTIONARY_THEME
)

existing_labels_path_q = questionary.path(
    "Load Existing Labels (.json): ",
    file_filter=lambda x: x.endswith(".json"),
    style=QUESTIONARY_THEME,
)

main_menu_q = questionary.select(
    "What next?",
    choices=["Review Cluster", "Export Cluster Labels & Exit", "Exit"],
    style=QUESTIONARY_THEME,
)


def cluster_select_q(sorted_cluster_ids: List[str]) -> questionary.Question:
    return questionary.autocomplete(
        "Cluster ID:",
        choices=sorted_cluster_ids,
        validate=lambda x: (x in sorted_cluster_ids) or x == "",
        style=QUESTIONARY_THEME,
    )


cluster_menu_q = questionary.select(
    "What Next?",
    choices=[
        "View Cluster Examples",
        "Declare Name",
        "Return to Main Menu",
    ],
    style=QUESTIONARY_THEME,
)


def declare_name_q(cluster_names: List[str]) -> questionary.Question:
    if len(cluster_names) > 0:
        return questionary.autocomplete(
            "Cluster Name", choices=cluster_names, style=QUESTIONARY_THEME
        )
    return questionary.text("Cluster Name", style=QUESTIONARY_THEME)


export_path_q = questionary.path(
    "Export Filename (.json):",
    validate=lambda x: x.endswith(".json"),
    style=QUESTIONARY_THEME,
)
