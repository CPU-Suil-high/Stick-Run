from ctypes import *

user32 = windll.user32
kernel32 = windll.kernel32

class COORD(Structure):
    _fields_ = [("x", c_short), ("y", c_short)]

class CONSOLE_CURSOR_INFO(Structure):
    _fields_ = [("dwSize", c_ulong), ("bVisible", c_bool)]

STD_OUTPUT_HANDLE = -11
STD_INPUT_HANDLE = -10

ENABLE_QUICK_EDIT_MODE = 0x0040
ENABLE_EXTENDED_FLAGS = 0x0080

class Color:
    BLACK = 0
    DARK_BLUE = 1
    DARK_GREEN = 2
    DARK_SKYBLUE = 3
    DARK_RED = 4
    DARK_VOILET = 5
    DARK_YELLOW = 6
    GRAY = 7
    DARK_GRAY = 8
    BLUE = 9
    GREEN = 10
    SKYBLUE = 11
    RED = 12
    VIOLET = 13
    YELLOW = 14
    WHITE = 15
    DEFAULT_TEXT_COLOR = WHITE
    DEFAULT_BACKGROUND_COLOR = BLACK

class VirtualKey:
    LBUTTON = 0x01
    "Left mouse button"
    RBUTTON = 0x02
    "Right mouse button"
    CANCEL = 0x03
    "Ctrl + Break"
    MBUTTON = 0x04
    "Mddle mouse button"
    XBUTTON1 = 0x05
    "x1 mouse button"
    XBUTTON2 = 0x06
    "x2 mouse button"
    BACK = 0x08
    "Backspace"
    TAB = 0x09
    CLEAR = 0xC
    RETURN = 0xD
    "Enter"
    SHIFT = 0x10
    CONTROL = 0x11
    "Ctrl"
    MENU = 0x12
    "Alt"
    PAUSE = 0x13
    "Pause Break"
    CAPITAL = 0x14
    "Caps Lock"
    ESCAPE = 0x1B
    SPACE = 0x20
    PRIOR = 0x21
    "Page Up"
    NEXT = 0x22
    "Page Down"
    END = 0x23
    HOME = 0x24
    LEFT = 0x25
    UP = 0x26
    RIGHT = 0x27
    DOWN = 0x28
    SELECT = 0x29
    PRINT = 0x2A
    EXECUTE = 0x2B
    SNAPSHOT = 0x2C
    INSERT = 0x2D
    DELETE = 0x2E
    HELP = 0x2F
    ZERO = 0x30
    ONE = 0x31
    TWO = 0x32
    THREE = 0x33
    FOUR = 0x34
    FIVE = 0x35
    SIX = 0x36
    SEVEN = 0x37
    EIGHT = 0x38
    NINE = 0x39
    A = 0x41
    B = 0x42
    C = 0x43
    D = 0x44
    E = 0x45
    F = 0x46
    G = 0x47
    H = 0x48
    I = 0x49
    J = 0x4A
    K = 0x4B
    L = 0x4C
    M = 0x4D
    N = 0x4E
    O = 0x4F
    P = 0x50
    Q = 0x51
    R = 0x52
    S = 0x53
    T = 0x54
    U = 0x55
    V = 0x56
    W = 0x57
    X = 0x58
    Y = 0x59
    Z = 0x5A

def printf(object) -> None:
    if (type(object) == bytes):
        cdll.msvcrt.printf(object)
    else:
        text = str(object)
        cdll.msvcrt.printf(text.encode("cp949"))

def gotoxy(x:int, y:int) -> None:
    handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    kernel32.SetConsoleCursorPosition(handle, COORD(x, y))

def hideCursor() -> None:
    handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    info = CONSOLE_CURSOR_INFO()
    info.dwSize = 100
    info.bVisible = 0

    kernel32.SetConsoleCursorInfo(handle, byref(info))

def setQuickEditMode(enable:bool) -> None:
    handle = kernel32.GetStdHandle(STD_INPUT_HANDLE)

    consoleMode = c_uint32()

    kernel32.GetConsoleMode(handle, byref(consoleMode))

    if (enable):
        consoleMode = consoleMode.value | ENABLE_QUICK_EDIT_MODE
    else:
        consoleMode = consoleMode.value & (~ ENABLE_QUICK_EDIT_MODE)
    
    consoleMode = consoleMode | ENABLE_EXTENDED_FLAGS

    kernel32.SetConsoleMode(handle, consoleMode)

def setColor(textColor:int, backgroundColor:int) -> None:
    handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    kernel32.SetConsoleTextAttribute(handle, textColor | (backgroundColor << 4))

def getAsyncKeyState(key:int) -> int:
    return user32.GetAsyncKeyState(key)

def getPressedKey(key:int) -> bool:
    if (user32.GetAsyncKeyState(key) & 0x8001):
        return True
    else:
        return False