from edit_box import EditBox
from user32 import *
from button import Button
from pathlib import Path
from os import listdir

buttons = []
BTN_WIDTH = 300
BTN_HEIGHT = 100
LINES = 10
PASSWORD_BOX_ID = 210
PASSWORD_SUBMIT_ID = 211
PASSWORD_CLOSE_ID = 212

@WNDPROC
def ChildWindowProc(hwnd, uMsg, wParam, lParam):
    match uMsg:
        case WindowMessage.DESTROY:
            print("ran")
            parent = user32.GetParent(hwnd)
            result = user32.EnableWindow(parent, 1)
        case WindowMessage.CLOSE:
            parent = user32.GetParent(hwnd)
            result = user32.EnableWindow(parent, 1)
            DestroyWindow(hwnd)

        case WindowMessage.COMMAND:
            control_id = LOWORD(wParam).value
            notification_code = HIWORD(wParam).value
            control_hwnd = lParam
            if control_id == PASSWORD_SUBMIT_ID:
                print("submit clicked")
                password = get_password(hwnd)
                
    return DefWindowProcA(hwnd, uMsg, wParam, lParam)

@WNDPROC
def WindowProc(hwnd, uMsg, wParam, lParam):
    si = SCROLLINFO()
    si_pointer = pointer(si)
    match uMsg:
        case WindowMessage.CREATE:
            create_list_of_buttons(get_files(), hwnd)
        case WindowMessage.DESTROY:
            PostQuitMessage(0)
            return 0
        
        case WindowMessage.SIZE:
            height = (HIWORD(lParam))
            width = (LOWORD(lParam))

            si.cbSize = sizeof(si)
            si.fMask = ScrollInfoMessage.RANGE | ScrollInfoMessage.PAGE
            si.nMin = 0
            si.nMax = BTN_HEIGHT * 5 - 60
            si.nPage = 1;
            SetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer, True)

        case WindowMessage.COMMAND:
            if wParam >= 100:
                btn_clicked = ([button for button in buttons if button.hMenu == wParam])
                filename = btn_clicked[0].btn_text
                password_hwnd = display_password_box(hwnd)
        case WindowMessage.VSCROLL:
            si.cbSize = sizeof(si)
            si.fMask = ScrollInfoMessage.ALL
            GetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer)

            yPos = si.nPos
            match LOWORD(wParam).value:
                case ScrollBarCommands.LINEUP:
                    si.nPos -= 1
                case ScrollBarCommands.TOP:
                    si.nPos = si.nMin
                case ScrollBarCommands.BOTTOM:
                    si.nPos = si.nMax
                case ScrollBarCommands.LINEUP:
                    si.nPos -= 1
                case ScrollBarCommands.LINEDOWN:
                    si.nPos += 1
                case ScrollBarCommands.PAGEUP:
                    si.nPos -= si.nPage
                case ScrollBarCommands.PAGEDOWN:
                    si.nPos += si.nPage
                case ScrollBarCommands.THUMBTRACK:
                    si.nPos = si.nTrackPos

            si.fMask = ScrollInfoMessage.POS
            SetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer, True)
            GetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer)
            if(si.nPos != yPos):
                ScrollWindowEx(hwnd, -0, (yPos - si.nPos), None, None, None, None, 0x0001|0x0002)
                hdwp = BeginDeferWindowPos(1)
                recent_hdwp = DeferWindowPos(hdwp, hwnd, None,  0, 0, 100, 100, 0x0020|0x0004|0x0001|0x0002)
                EndDeferWindowPos(recent_hdwp)

    return DefWindowProcA(hwnd, uMsg, wParam, lParam)

def get_files():
    folder_path = Path(__file__).parent / "log"
    return [file for file in listdir(folder_path) if file.endswith(".txt")]

def create_list_of_buttons(filenames: list[str], parent_window):
    """
    Makes a list of button that have the file's name as their heading
    """
    x, y = 0, 0
    for button_id, filename in enumerate(filenames, 100):
        button = Button(bytes(filename, "utf-8"), x, y, BTN_WIDTH, BTN_HEIGHT, parent_window, button_id)
        button.create_button()
        buttons.append(button)
        y += BTN_HEIGHT

    return buttons

def get_password(hwnd):
    password = create_string_buffer(100)
    dialog_box = GetDlgItem(hwnd, PASSWORD_BOX_ID)
    SendMessageA(dialog_box, 0x000D, WPARAM(100), LPARAM(cast(password, c_void_p).value))
    print(password.value)
    

def display_password_box(hwndParent):
    dialog_box = create_child_window(hwndParent, "Password", ChildWindowProc, 350, 200)
    password_box = EditBox(dialog_box
        ,PASSWORD_BOX_ID
        ,""
        ,[
         WindowStyles.TABSTOP
        |WindowStyles.BORDER
        |WindowStyles.VISIBLE
        |WindowStyles.CHILD
        |ButtonStyle.TEXT
        |EditStyles.PASSWORD
        ]
        ,10
        ,10
        ,315
        ,40).create_edit_box()
    submit_button = Button(bytes("Submit", encoding = "utf-8"), 200, 100, 70, 30, dialog_box, 211).create_button()
    close_button = Button(bytes("Close", encoding="utf-8"), 20, 100, 70, 30, dialog_box, PASSWORD_CLOSE_ID).create_button()
    ShowWindow(dialog_box, 5)
    return dialog_box

def create_control_box(hwnd_parent, window_type, control_id, x, y, width, height, text = ""):
    hwnd_box = CreateWindowExA(
        0,
        bytes(window_type, encoding="utf-8"),
        bytes(text, encoding="utf-8"),
        WindowStyles.TABSTOP|
        WindowStyles.BORDER
        | WindowStyles.VISIBLE
        | WindowStyles.CHILD
        | ButtonStyle.TEXT
        | EditStyles.PASSWORD,
        x,
        y,
        width,
        height,
        hwnd_parent,
        HMENU(control_id),
        cast(GetWindowLongPtrA(hwnd_parent, GetWindowLong.HINSTANCE), HINSTANCE),
        None,
    )

    return hwnd_box


def create_child_window(hWndParent, window_name, window_proc, width, height):
    hinstance = GetModuleHandleA(None)
    child_class_name = b'child window'
    window_class = WNDCLASSA()
    window_class.style = ClassStyles.VREDRAW | ClassStyles.HREDRAW
    window_class.lpfnWndProc = window_proc
    window_class.hInstance = hinstance
    window_class.lpszClassName = child_class_name
    window_class.hbrBackground = HBRUSH(5)
    window_class.hIcon = None

    RegisterClassA(byref(window_class))

    hwnd_child = CreateWindowExA(
        0,
        child_class_name,
        bytes(window_name, encoding="utf-8"),
        WindowStyles.OVERLAPPED | WindowStyles.CAPTION
        | WindowStyles.SYSMENU | WindowStyles.MINIMIZEBOX,
        CW_USEDEFAULT, CW_USEDEFAULT, width, height,
        hWndParent,
        None,
        hinstance,
        None
    )
    return hwnd_child

def main():
    class_name = b"Hello world!"
    hinstance = GetModuleHandleA(None)

    window_class = WNDCLASSA()
    window_class.style = ClassStyles.VREDRAW | ClassStyles.HREDRAW
    window_class.lpfnWndProc = WindowProc
    window_class.hInstance = hinstance
    window_class.lpszClassName = class_name
    window_class.hbrBackground = HBRUSH(5)
    window_class.hIcon = None
    RegisterClassA(byref(window_class))

    hwnd_main = CreateWindowExA(
        0,
        class_name,
        b"Example",
        WindowStyles.OVERLAPPED
        | WindowStyles.CAPTION
        | WindowStyles.SYSMENU
        | WindowStyles.MINIMIZEBOX,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        600,
        480,
        None,
        None,
        hinstance,
        None,
    )

    client_rect = RECT()
    GetClientRect(hwnd_main, byref(client_rect))

    ShowWindow(hwnd_main, 5)

    msg = MSG()
    while (bRet := GetMessageA(byref(msg), None, 0, 0)) != 0:
        if bRet == -1:
            break
        TranslateMessage(byref(msg))
        DispatchMessageA(byref(msg))


main()
