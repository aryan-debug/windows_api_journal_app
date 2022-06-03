from user32 import *


class ControlBox:
    def __init__(self, hwndParent, control_type, id):
        self.hwndParent = hwndParent
        self.control_type = control_type
        self.id = id

    def create_control_box(self):
        return CreateWindowExA(
            0,
            bytes(self.control_type, encoding="utf-8"),
            bytes(self.text, encoding="utf-8"),
            *self.styles,
            self.x,
            self.y,
            self.width,
            self.height,
            self.hwndParent,
            HMENU(self.id),
            cast(
                GetWindowLongPtrA(self.hwndParent, GetWindowLong.HINSTANCE), HINSTANCE
            ),
            None,
        )

    def set_styles(self, styles):
        self.styles = styles

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def set_text(self, text):
        self.text = text
