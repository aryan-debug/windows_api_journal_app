from turtle import clear, onclick
import wingui
from pathlib import Path
import os
from win32.user32 import *
import cryptocode

msg_handler = wingui.MessageHandler()
main_window = wingui.Window(msg_handler, "Main", (480, 600))

BTN_HEIGHT = 100
BTN_WIDTH = 300


LOG_PATH = Path(__file__).parent / "log"


def destroy_window(hwnd, lparam):
    if hwnd:
        DestroyWindow(hwnd)

    return True


def clear_screen(hwnd, callback_func, lparam):
    EnumChildWindows(hwnd, WNDENUMPROC(callback_func), lparam)


def get_files():
    return [file for file in os.listdir(LOG_PATH) if file.endswith(".txt")]


def get_file_content(filename):
    file_path = LOG_PATH / filename
    with open(file_path, "r") as file:
        return "".join([line.strip() for line in file.readlines()])


def decrypt_file_content(file_content, password):
    return cryptocode.decrypt(file_content, password)


def make_password_box(parent):
    dialog_box = wingui.Window(msg_handler, "Password", (300, 150), parent=parent)
    password_box = wingui.EditText(
        dialog_box, "", (10, 10), (260, 50), WindowStyle.BORDER | 0x0020
    )
    submit_button = wingui.Button(
        dialog_box,
        "Submit",
        (150, 70),
        (70, 30),
        ButtonStyle.PUSHBUTTON,
    )
    close_button = wingui.Button(
        dialog_box,
        "Close",
        (50, 70),
        (70, 30),
        ButtonStyle.PUSHBUTTON,
        onclick=lambda: parent.close(),
    )
    return (dialog_box, password_box, submit_button, close_button)


def password_submit_button_handler(dialog_box, password_box, folder_path, plain_text):
    def func():
        password = password_box.get_text()
        encrypted_text = cryptocode.encrypt(plain_text, password)
        with open(folder_path, "w") as file:
            file.write(encrypted_text)

    return func


def save_encrypted_file(filename, file_display):
    def func():
        folder_path = LOG_PATH / filename
        plain_text = file_display.get_text()
        dialog_box, password_box, submit_button, close_button = make_password_box(
            main_window
        )
        dialog_box.show()
        submit_button.onclick = password_submit_button_handler(
            dialog_box, password_box, folder_path, plain_text
        )

    return func


def make_file_content_gui(content, filename):
    file_display = wingui.EditText(
        main_window,
        content,
        (10, 10),
        (300, 300),
        WindowStyle.BORDER
        | EditStyles.MULTILINE
        | WindowStyle.VSCROLL
        | WindowStyle.HSCROLL,
    )
    save_button = wingui.Button(
        main_window,
        "Save",
        (100, 350),
        (70, 30),
        ButtonStyle.PUSHBUTTON,
        onclick=save_encrypted_file(filename, file_display),
    )


def display_file(button, dialog_box, edit_box):
    def func():
        if dialog_box:
            clear_screen(main_window.handle, destroy_window, 0)
            filename = button.text
            password = edit_box.get_text()
            file_content = get_file_content(filename)
            decrypted = decrypt_file_content(file_content, password)
            if not decrypted:
                decrypted = "WRONG PASSWORD"
            dialog_box.close()
            make_file_content_gui(decrypted, filename)
        else:
            clear_screen(main_window.handle, destroy_window, 0)
            make_file_content_gui("", button.text)

    return func


def display_dialog_box(button):
    def create_dialog_box():
        file = LOG_PATH / button.text
        is_file_empty = os.path.getsize(file) == 0
        if not is_file_empty:
            (
                dialog_box,
                password_edit_box,
                submit_button,
                close_button,
            ) = make_password_box(main_window)

            submit_button.onclick = display_file(button, dialog_box, password_edit_box)

            dialog_box.show()
        else:
            display_file(button, None, None)()

    return create_dialog_box


def create_list_of_buttons(filenames: list[str], parent_window):
    """
    Makes a list of button that have the file's name as their heading
    """
    x, y = 0, 0
    for filename in filenames:
        button = wingui.Button(
            parent_window,
            filename,
            (x, y),
            (BTN_WIDTH, BTN_HEIGHT),
            ButtonStyle.PUSHBUTTON,
        )
        button.onclick = display_dialog_box(button)
        y += BTN_HEIGHT


if __name__ == "__main__":
    create_list_of_buttons(get_files(), main_window)
    main_window.show()
    msg_handler.run()
