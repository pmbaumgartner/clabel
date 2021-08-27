from rich.theme import Theme
from questionary import Style

# https://rich.readthedocs.io/en/stable/style.html#style-themes
# https://questionary.readthedocs.io/en/stable/pages/advanced.html#themes-styling

GREEN = "#00997b"
CORAL = "#fc766a"
RED = "#e34f33"

RICH_THEME = Theme(
    {
        "emphasis": f"bold {GREEN}",
        "input": f"{CORAL}",
        "warning": f"bold {RED} on white",
        "kb": "black on white",
    }
)
QUESTIONARY_THEME = Style(
    [
        ("qmark", f"fg:{GREEN} bold"),  # token in front of the question
        ("question", "bold"),  # question text
        ("answer", f"fg:{CORAL} bold"),  # submitted answer text behind the question
        ("pointer", f"fg:{CORAL} bold"),  # pointer used in select and checkbox prompts
        (
            "highlighted",
            f"fg:{CORAL} bold",
        ),  # pointed-at choice in select and checkbox prompts
        ("selected", f"fg:{CORAL}"),  # style for a selected item of a checkbox
        ("separator", f"fg:{CORAL}"),  # separator in lists
    ]
)
