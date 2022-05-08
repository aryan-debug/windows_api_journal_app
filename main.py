from os import listdir
from user32 import *
from button import Button
from pathlib import Path

hInst = windll.kernel32.GetModuleHandleW(0)
buttons = []

BTN_WIDTH = 300
BTN_HEIGHT = 100
LINES = 28

def window_proc(hwnd: HWND, umsg: UINT, wparam: WPARAM, lparam: LPARAM) -> LRESULT:
    si = SCROLLINFO()
    si_pointer = pointer(si)
    match umsg:
        case WindowMessage.CREATE:
            create_list_of_buttons(get_files(), hwnd)
        case WindowMessage.DESTROY:
            PostQuitMessage(0)
            return 0
        
        case WindowMessage.SIZE:
            height = (HIWORD(lparam))
            width = (LOWORD(lparam))

            si.cbSize = sizeof(si)
            si.fMask = ScrollInfoMessage.RANGE | ScrollInfoMessage.PAGE
            si.nMin = 0
            si.nMax = LINES
            si.nPage = height.value // BTN_HEIGHT;
            SetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer, True)

        case WindowMessage.COMMAND:
            if wparam >= 100:
                btn_clicked = ([button for button in buttons if button.hMenu == wparam])
                filename = btn_clicked[0].btn_text
                print(filename)
                rect = RECT()
                rect_p = pointer(rect)
                print(GetClientRect(hwnd, rect_p))
                print(rect.top, rect.bottom, rect.left, rect.right)
        case WindowMessage.VSCROLL:
            si.cbSize = sizeof(si)
            si.fMask = ScrollInfoMessage.ALL
            GetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer)

            yPos = si.nPos
            match LOWORD(wparam).value:
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
                    print(si.nPos)
                    si.nPos = si.nTrackPos
                    print(si.nPos)

            si.fMask = ScrollInfoMessage.POS
            SetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer, True)
            GetScrollInfo(hwnd, ScrollBarConstants.VERT, si_pointer)
            if(si.nPos != yPos):
                ScrollWindowEx(hwnd, -0, (yPos - si.nPos), None, None, None, None, 0x0002|0x0004)
                UpdateWindow(hwnd)

    return DefWindowProcW(hwnd, umsg, wparam, lparam)


def create_window(className, windowName):
    wnd_main = CreateWindowExW(
        0,
        className,
        windowName,
        WindowStyles.OVERLAPPED
        | WindowStyles.CAPTION
        | WindowStyles.SYSMENU
        | WindowStyles.THICKFRAME
        | WindowStyles.MINIMIZEBOX
        | WindowStyles.MAXIMIZEBOX
        | WindowStyles.CAPTION
        | WindowStyles.VSCROLL,
        CW_USEDEFAULT,
        CW_USEDEFAULT,
        600,
        600,
        0,
        0,
        hInst,
        0,
    )
    if not wnd_main:
        print("Window Creation Falid: ", GetLastError())
        return
    return wnd_main


def get_files():
    folder_path = Path(__file__).parent / "log"
    return [file for file in listdir(folder_path) if file.endswith(".txt")]

def create_list_of_buttons(filenames: list[str], parent_window):
    """
    Makes a list of button that have the file's name as their heading
    """
    x, y = 0, 0
    for button_id, filename in enumerate(filenames, 100):
        button = Button(filename, x, y, BTN_WIDTH, BTN_HEIGHT, parent_window, button_id)
        button.create_button()
        buttons.append(button)
        y += BTN_HEIGHT

    return buttons




def main():
    wclassName = ctypes.c_wchar_p("My")
    wname = ctypes.c_wchar_p("Left")
    wndClass = WNDCLASSEXW()
    wndClass.cbSize = sizeof(WNDCLASSEXW)
    wndClass.style = ClassStyles.HREDRAW | ClassStyles.VREDRAW
    wndClass.lpfnWndProc = WNDPROC(window_proc)
    wndClass.cbClsExtra = 0
    wndClass.cbWndExtra = 0
    wndClass.hInstance = hInst
    wndClass.hIcon = 0
    wndClass.hCursor = 0
    wndClass.hBrush = windll.gdi32.GetStockObject(0)
    wndClass.lpszMenuName = 0
    wndClass.lpszClassName = wclassName
    wndClass.hIconSm = 0
    RegisterClassExW(byref(wndClass))
    wnd_main = create_window(wclassName, wname)
    ShowWindow(wnd_main, 5)
    UpdateWindow(wnd_main)

    msg = MSG()
    lpmsg = pointer(msg)
    while (GetMessageW(lpmsg, 0, 0, 0)) != 0:
        TranslateMessage(lpmsg)
        DispatchMessageW(lpmsg)


main()
