from ctypes.wintypes import HINSTANCE, HMENU, HWND, LPCWSTR, LPVOID
from dataclasses import dataclass
from ctypes import *

from user32 import (
    ButtonStyle,
    CreateWindowExA,
    GetWindowLongPtrA,
    WindowStyles,
    GetWindowLong,
)


@dataclass
class Button:
    btn_text: LPCWSTR
    x: c_int
    y: c_int
    width: c_int
    height: c_int
    hwnd_parent: HWND
    hMenu: HMENU

    def create_button(self):
        button = CreateWindowExA(
            0,
            b"BUTTON",
            self.btn_text,
            WindowStyles.VISIBLE | WindowStyles.CHILD | ButtonStyle.PUSHBUTTON,
            self.x,
            self.y,
            self.width,
            self.height,
            self.hwnd_parent,
            HMENU(self.hMenu),
            cast(
                GetWindowLongPtrA(self.hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE
            ),
            None,
        )

        return button
