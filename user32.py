import enum
from ctypes import *
from ctypes.wintypes import *

WNDPROC = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)
LRESULT = c_long
LONG_PTR = LPARAM
CW_USEDEFAULT = 0x80000000
WNDENUMPROC = WINFUNCTYPE(BOOL, HWND, LPARAM)
DLGPROC = WINFUNCTYPE(POINTER(c_int), HWND, c_uint, WPARAM, LPARAM)
MAKEINTRESOURCE = lambda i: LPWSTR(POINTER(ULONG(WORD(i))))
HCURSOR = HANDLE
user32 = windll.user32
DIALOG_BTN = 101


def LPVOID_errcheck(result, func, args):
    if not result:
        raise WinError()
    return result


class WindowStyles(enum.IntFlag):
    BORDER = 0x00800000
    CAPTION = 0x00C00000
    CHILD = 0x40000000
    CHILDWINDOW = 0x40000000
    CLIPCHILDREN = 0x02000000
    CLIPSIBLINGS = 0x04000000
    DISABLED = 0x08000000
    DLGFRAME = 0x00400000
    GROUP = 0x00020000
    HSCROLL = 0x00100000
    ICONIC = 0x20000000
    MAXIMIZE = 0x01000000
    MAXIMIZEBOX = 0x00010000
    MINIMIZE = 0x20000000
    MINIMIZEBOX = 0x00020000
    OVERLAPPED = 0x00000000
    SYSMENU = 0x00080000
    THICKFRAME = 0x00040000
    TILED = 0x00000000
    VISIBLE = 0x10000000
    VSCROLL = 0x00200000
    SIZEBOX = 0x00040000
    TABSTOP = 0x00010000
    POPUP = 0x80000000
    TILEDWINDOW = (
        OVERLAPPED | CAPTION | SYSMENU | THICKFRAME | MINIMIZEBOX | MAXIMIZEBOX
    )
    OVERLAPPEDWINDOW = (
        OVERLAPPED | CAPTION | SYSMENU | THICKFRAME | MINIMIZEBOX | MAXIMIZEBOX
    )
    POPUPWINDOW = POPUP | BORDER | SYSMENU


class WindowMessage(enum.IntEnum):
    SETFOCUS = 0x0007
    KILLFOCUS = 0x0006
    ENABLE = 0x000A
    SETREDRAW = 0x000B
    SETTEXT = 0x000C
    SETFONT = 0x0030
    GETFONT = 0x0031
    GETTEXT = 0x000D
    GETTEXTLENGTH = 0x000E
    PAINT = 0x000F
    CLOSE = 0x00010
    QUIT = 0x0012
    SHOWWINDOW = 0x0018
    NULL = 0x0000
    CREATE = 0x0001
    DESTROY = 0x0002
    MOVE = 0x0003
    SIZE = 0x0005
    ACTIVATE = 0x0006
    COMMAND = 0x0111
    NOTIFY = 0x004E
    VSCROLL = 0x0115


class ClassStyles(enum.IntFlag):
    VREDRAW = 0x0001
    HREDRAW = 0x0002
    DBLCLKS = 0x0008
    OWNDC = 0x0020
    CLASSDC = 0x0040
    PARENTDC = 0x0080
    NOCLOSE = 0x0200
    SAVEBITS = 0x0800
    BYTEALIGNCLIENT = 0x1000
    BYTEALIGNWINDOW = 0x2000
    GLOBALCLASS = 0x4000


class ButtonStyle(enum.IntFlag):
    PUSHBUTTON = 0x00000000
    DEFPUSHBUTTON = 0x00000001
    CHECKBOX = 0x00000002
    AUTOCHECKBOX = 0x00000003
    RADIOBUTTON = 0x00000004
    _3STATE = 0x00000005
    AUTO3STATE = 0x00000006
    GROUPBOX = 0x00000007
    USERBUTTON = 0x00000008
    AUTORADIOBUTTON = 0x00000009
    PUSHBOX = 0x0000000A
    OWNERDRAW = 0x0000000B
    TYPEMASK = 0x0000000F
    LEFTTEXT = 0x00000020
    TEXT = 0x00000000
    ICON = 0x00000040
    BITMAP = 0x00000080
    LEFT = 0x00000100
    RIGHT = 0x00000200
    CENTER = 0x00000300
    TOP = 0x00000400
    BOTTOM = 0x00000800
    VCENTER = 0x00000C00
    PUSHLIKE = 0x00001000
    MULTILINE = 0x00002000
    NOTIFY = 0x00004000
    FLAT = 0x00008000
    RIGHTBUTTON = LEFTTEXT


class EditStyles(enum.IntFlag):
    LEFT = 0x0000
    CENTER = 0x0001
    RIGHT = 0x0002
    MULTILINE = 0x0004
    UPPERCASE = 0x0008
    LOWERCASE = 0x0010
    PASSWORD = 0x0020
    AUTOVSCROLL = 0x0040
    AUTOHSCROLL = 0x0080
    NOHIDESEL = 0x0100
    OEMCONVERT = 0x0400
    READONLY = 0x0800
    WANTRETURN = 0x1000
    NUMBER = 0x2000


class WNDCLASSA(Structure):
    _fields_ = [
        ("style", UINT),
        ("lpfnWndProc", WNDPROC),
        ("cbClsExtra", c_int),
        ("cbWndExtra", c_int),
        ("hInstance", HINSTANCE),
        ("hIcon", HICON),
        ("hCursor", HCURSOR),
        ("hbrBackground", HBRUSH),
        ("lpszMenuName", LPCSTR),
        ("lpszClassName", LPCSTR),
    ]


class MSG(Structure):
    _fields_ = [
        ("hwnd", HWND),
        ("message", c_int),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", DWORD),
        ("pt", POINT),
        ("lPrivate", DWORD),
    ]


class GetWindowLong(enum.IntEnum):
    EXSTYLE = -20
    HINSTANCE = -6
    HWNDPARENT = -8
    ID = -12
    STYLE = -16
    USERDATA = -21
    WNDPROC = -4


class SCROLLINFO(Structure):
    _fields_ = [
        ("cbSize", UINT),
        ("fMask", UINT),
        ("nMin", c_int),
        ("nMax", c_int),
        ("nPage", UINT),
        ("nPos", c_int),
        ("nTrackPos", c_int),
    ]


class DLGTEMPLATE(Structure):
    _fields_ = [
        ("style", DWORD),
        ("dwExtendedStyle", DWORD),
        ("cdit", WORD),
        ("x", c_short),
        ("y", c_short),
        ("cx", c_short),
        ("cy", c_short),
    ]


class ScrollInfoMessage(enum.IntEnum):
    RANGE = 0x0001
    PAGE = 0x0002
    POS = 0x0004
    DISABLENOSCROLL = 0x0008
    TRACKPOS = 0x0010
    ALL = RANGE | PAGE | POS | TRACKPOS


class ScrollBarConstants(enum.IntEnum):
    HORZ = 0
    VERT = 1
    CTL = 2
    BOTH = 3


class ScrollBarCommands(enum.IntEnum):
    LINEUP = 0
    LINELEFT = 0
    LINEDOWN = 1
    LINERIGHT = 1
    PAGEUP = 2
    PAGELEFT = 2
    PAGEDOWN = 3
    PAGERIGHT = 3
    THUMBPOSITION = 4
    THUMBTRACK = 5
    TOP = 6
    LEFT = 6
    BOTTOM = 7
    RIGHT = 7
    ENDSCROLL = 8


def HIWORD(l):
    return WORD((l >> 16) & 0xFFFF)


def LOWORD(l):
    return WORD(l & 0xFFFF)


LPMSG = POINTER(MSG)
LPCSCROLLINFO = POINTER(SCROLLINFO)

DefWindowProcA = user32.DefWindowProcA
DefWindowProcA.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProcA.restype = LRESULT

CreateWindowExA = user32.CreateWindowExA
CreateWindowExA.argtypes = [
    DWORD,
    LPCSTR,
    LPCSTR,
    DWORD,
    c_int,
    c_int,
    c_int,
    c_int,
    HWND,
    HMENU,
    HINSTANCE,
    LPVOID,
]
CreateWindowExA.restype = HWND
CreateWindowExA.errcheck = LPVOID_errcheck

LPWNDCLASSA = POINTER(WNDCLASSA)

GetModuleHandleA = windll.kernel32.GetModuleHandleA
GetModuleHandleA.argtypes = [LPCSTR]
GetModuleHandleA.restype = HMODULE
GetModuleHandleA.errcheck = LPVOID_errcheck

RegisterClassA = user32.RegisterClassA
RegisterClassA.argtypes = [LPWNDCLASSA]
RegisterClassA.restype = ATOM
RegisterClassA.errcheck = LPVOID_errcheck

ShowWindow = user32.ShowWindow
ShowWindow.argtypes = [HWND, c_int]
ShowWindow.restype = BOOL

UpdateWindow = user32.UpdateWindow
UpdateWindow.argtypes = [HWND]
UpdateWindow.restype = BOOL

GetMessageA = user32.GetMessageA
GetMessageA.argtypes = [LPMSG, HWND, UINT, UINT]
GetMessageA.restype = BOOL

TranslateMessage = user32.TranslateMessage
TranslateMessage.argtypes = [LPMSG]
TranslateMessage.restype = BOOL

DispatchMessageA = user32.DispatchMessageA
DispatchMessageA.argtypes = [LPMSG]
DispatchMessageA.restype = BOOL

PostQuitMessage = user32.PostQuitMessage
PostQuitMessage.argtypes = [c_int]
PostQuitMessage.restype = None

try:
    GetWindowLongPtrA = user32.GetWindowLongPtrA
except:
    GetWindowLongPtrA = user32.GetWindowLongA
GetWindowLongPtrA.argtypes = [HWND, c_int]
GetWindowLongPtrA.restype = LONG_PTR
GetWindowLongPtrA.errcheck = LPVOID_errcheck

GetWindow = user32.GetWindow
GetWindow.argtypes = [HWND, UINT]
GetWindow.restype = HWND

ScrollWindowEx = user32.ScrollWindowEx
ScrollWindowEx.argtypes = [HWND, c_int, c_int, LPRECT, LPRECT, HRGN, LPRECT, UINT]
ScrollWindowEx.restype = int

SetScrollInfo = user32.SetScrollInfo
SetScrollInfo.argtypes = [HWND, c_int, LPCSCROLLINFO, BOOL]
SetScrollInfo.restype = int

GetScrollInfo = user32.GetScrollInfo
GetScrollInfo.argtypes = [HWND, c_int, LPCSCROLLINFO]
GetScrollInfo.restype = BOOL

GetClientRect = user32.GetClientRect
GetClientRect.argtypes = [HWND, LPRECT]
GetClientRect.restype = BOOL

BeginDeferWindowPos = user32.BeginDeferWindowPos
BeginDeferWindowPos.argtypes = [c_int]
BeginDeferWindowPos.restype = HDWP

DeferWindowPos = user32.DeferWindowPos
DeferWindowPos.argtypes = [HDWP, HWND, HWND, c_int, c_int, c_int, c_int, c_uint]
DeferWindowPos.restype = HDWP

EndDeferWindowPos = user32.EndDeferWindowPos
EndDeferWindowPos.argtypes = [HDWP]
EndDeferWindowPos.restype = BOOL

DestroyWindow = user32.DestroyWindow
DestroyWindow.argtypes = [HWND]
DestroyWindow.restype = BOOL

EnumChildWindows = user32.EnumChildWindows
EnumChildWindows.argtypes = [HWND, WNDENUMPROC, LPARAM]
EnumChildWindows.restype = BOOL

SendMessageA = user32.SendMessageA
SendMessageA.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessageA.restype = LRESULT

GetWindow = user32.GetWindow
GetWindow.argtypes = [HWND, UINT]
GetWindow.restype = HWND

GetWindowTextA = user32.GetWindowTextA
GetWindowTextA.argtypes = [HWND, LPSTR, c_int]
GetWindowTextA.restype = c_int

GetDlgItem = user32.GetDlgItem
GetDlgItem.argtypes = [HWND, c_int]
GetDlgItem.restype = HWND
