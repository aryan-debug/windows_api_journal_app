from button import Button
from pathlib import Path
from os import listdir

BTN_WIDTH = 300
BTN_HEIGHT = 100


def get_files():
    folder_path = Path(__file__).parent / "log"
    return [file for file in listdir(folder_path) if file.endswith(".txt")]


def create_list_of_buttons(filenames: list[str], parent_window):
    """
    Makes a list of button that have the file's name as their heading
    """
    buttons = []
    x, y = 0, 0
    for button_id, filename in enumerate(filenames, 100):
        button = Button(
            bytes(filename, "utf-8"),
            x,
            y,
            BTN_WIDTH,
            BTN_HEIGHT,
            parent_window,
            button_id,
        )
        button.create_button()
        buttons.append(button)
        y += BTN_HEIGHT

    return buttons
