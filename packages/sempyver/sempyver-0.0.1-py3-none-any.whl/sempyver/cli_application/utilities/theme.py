"""
Custom inquirer theme.
"""
from blessed import Terminal
from inquirer.themes import Default

term = Terminal()


class CustomTheme(Default):  # noqa
    """Custom Inquired theme to use for the Changeset CLI application"""

    def __init__(self):
        super().__init__()
        self.Question.brackets_color = term.blue + term.bold
        self.Question.mark_color = term.green + term.bold
        self.Checkbox.selection_icon = "❯"
        self.Checkbox.selection_color = term.blue + term.bold
        self.Checkbox.selected_icon = "◉"
        self.Checkbox.selected_color = term.green
        self.Checkbox.unselected_icon = "◯"
        self.List.selection_color = term.blue + term.bold
        self.List.selection_cursor = "❯"
