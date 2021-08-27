import pandas as pd
import questionary
from pathlib import Path
import json
from clabel.styles import QUESTIONARY_THEME

from typing import Tuple, Dict, List


def get_str_columns_and_max_len(df: pd.DataFrame) -> Tuple[List[str], str]:
    string_columns = list(df.select_dtypes("object").columns)
    longest_column = max(
        [(df[c].str.len().mean(), c) for c in string_columns], key=lambda x: x[0]
    )[1]
    return string_columns, longest_column


def get_column_info(df: pd.DataFrame) -> Tuple[str, str]:
    string_columns, longest_column = get_str_columns_and_max_len(df)
    # TODO: Refactor back into questions.py?
    text_column = questionary.select(
        "Select Text Column:",
        choices=string_columns,
        default=longest_column,
        style=QUESTIONARY_THEME,
    ).ask()
    non_text_columns = [col for col in df.columns if col != text_column]
    cluster_column = questionary.select(
        "Select Cluster ID Column:",
        choices=non_text_columns,
        style=QUESTIONARY_THEME,
    ).ask()
    return text_column, cluster_column


from typing import TypedDict


class ExportData(TypedDict):
    cluster_labels: Dict[int, str]
    text_column: str
    cluster_column: str


def export_summary(
    cluster_labels: Dict[int, str], text_column: str, cluster_column: str, filepath: str
) -> str:
    export_data: ExportData = {
        "cluster_labels": cluster_labels,
        "text_column": text_column,
        "cluster_column": cluster_column,
    }
    Path(filepath).write_text(json.dumps(export_data, indent=4))
    return filepath


def import_summary(filepath: str) -> Tuple[Dict[int, str], str, str]:
    import_data = json.loads(Path(filepath).read_text())
    cluster_labels = {int(k): v for k, v in import_data["cluster_labels"].items()}
    text_column = import_data["text_column"]
    cluster_column = import_data["cluster_column"]
    return cluster_labels, text_column, cluster_column
