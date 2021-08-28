"""
Author: Travis Hammond
Version: 3_19_2021
"""

from time import sleep, time
from copy import deepcopy
from threading import Event

import ctypes

from .capture import Capturer

SendInput = ctypes.windll.user32.SendInput
GetKeyState = ctypes.windll.user32.GetKeyState

KEY_MAP = {'ESC': 1, '1': 2, '2': 3, '3': 4, '4': 5, '5': 6, '6': 7,
           '7': 8, '8': 9, '9': 10, '0': 11, '-': 12, '=': 13,
           'BACKSPACE': 14, 'TAB': 15, 'q': 16, 'w': 17, 'e': 18, 'r': 19,
           't': 20, 'y': 21, 'u': 22, 'i': 23, 'o': 24, 'p': 25,
           '[': 26, ']': 27, 'NEWLINE': 28, 'CTRL': 29, 'a': 30,
           's': 31, 'd': 32, 'f': 33, 'g': 34, 'h': 35, 'j': 36,
           'k': 37, 'l': 38, ';': 39, "'": 40, '`': 41, 'LSHIFT': 42,
           '\\': 43, 'z': 44, 'x': 45, 'c': 46, 'v': 47, 'b': 48,
           'n': 49, 'm': 50, ',': 51, '.': 52, '/': 53, 'RSHIFT': 54,
           'PRINT': 55, 'ALT': 56, ' ': 57, 'CAPS': 58, 'F1': 59,
           'F2': 60, 'F3': 61, 'F4': 62, 'F5': 63, 'F6': 64, 'F7': 65,
           'F8': 66, 'F9': 67, 'F10': 68, 'NUM': 69, 'SCROLL': 70,
           'HOME': 71, 'UP': 72, 'PGUP': 73, '-2': 74, 'LEFT': 75,
           'CENTER': 76, 'RIGHT': 77, '+': 78, 'END': 79, 'DOWN': 80,
           'PGDN': 81, 'INSERT': 82, 'DELETE': 83}
SHIFTED_KEY_MAP = {'~': '`', '!': '1', '@': '2', '#': '3', '$': '4',
                   '%': '5', '^': '6', '&': '7', '*': '8', '(': '9',
                   ')': '0', '_': '-', '+': '=', '{': '[', '}': ']',
                   '|': '\\', ':': ';', '"': "'", '<': ',', '>': '.',
                   '?': '/'}

VK_KEY_MAP = {'LBUTTON': 0x01, 'RBUTTON': 0x02, 'CANCEL': 0x03,
              'MBUTTON': 0x04, 'XBUTTON1': 0x05, 'XBUTTON2': 0x06,
              'BACK': 0x08, 'TAB': 0x09, 'CLEAR': 0x0C, 'RETURN': 0x0D,
              'SHIFT': 0x10, 'CONTROL': 0x11, 'MENU': 0x12, 'PAUSE': 0x13,
              'CAPITAL': 0x14, 'KANA': 0x15, 'HANGUEL': 0x15, 'HANGUL': 0x15,
              'IME_ON': 0x16, 'JUNJA': 0x17, 'FINAL': 0x18, 'HANJA': 0x19,
              'KANJI': 0x19, 'IME_OFF': 0x1A, 'ESCAPE': 0x1B, 'CONVERT': 0x1C,
              'NONCONVERT': 0x1D, 'ACCEPT': 0x1E, 'MODECHANGE': 0x1F,
              'SPACE': 0x20, 'PRIOR': 0x21, 'NEXT': 0x22, 'END': 0x23,
              'HOME': 0x24, 'LEFT': 0x25, 'UP': 0x26, 'RIGHT': 0x27,
              'DOWN': 0x28, 'SELECT': 0x29, 'PRINT': 0x2A, 'EXECUTE': 0x2B,
              'SNAPSHOT': 0x2C, 'INSERT': 0x2D, 'DELETE': 0x2E, 'HELP': 0x2F,
              '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33,
              '4': 0x34, '5': 0x35, '6': 0x36, '7': 0x37,
              '8': 0x38, '9': 0x39, 'A': 0x41, 'B': 0x42, 'C': 0x43,
              'D': 0x44, 'E': 0x45, 'F': 0x46, 'G': 0x47, 'H': 0x48,
              'I': 0x49, 'J': 0x4A, 'K': 0x4B, 'L': 0x4C, 'M': 0x4D,
              'N': 0x4E, 'O': 0x4F, 'P': 0x50, 'Q': 0x51, 'R': 0x52,
              'S': 0x53, 'T': 0x54, 'U': 0x55, 'V': 0x56, 'W': 0x57,
              'X': 0x58, 'Y': 0x59, 'Z': 0x5A, 'LWIN': 0x5B, 'RWIN': 0x5C,
              'APPS': 0x5D, 'SLEEP': 0x5F, 'NUMPAD0': 0x60, 'NUMPAD1': 0x61,
              'NUMPAD2': 0x62, 'NUMPAD3': 0x63, 'NUMPAD4': 0x64,
              'NUMPAD5': 0x65, 'NUMPAD6': 0x66, 'NUMPAD7': 0x67,
              'NUMPAD8': 0x68, 'NUMPAD9': 0x69, 'MULTIPLY': 0x6A, 'ADD': 0x6B,
              'SEPARATOR': 0x6C, 'SUBTRACT': 0x6D, 'DECIMAL': 0x6E,
              'DIVIDE': 0x6F, 'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
              'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77, 'F9': 0x78,
              'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B, 'F13': 0x7C, 'F14': 0x7D,
              'F15': 0x7E, 'F16': 0x7F, 'F17': 0x80, 'F18': 0x81, 'F19': 0x82,
              'F20': 0x83, 'F21': 0x84, 'F22': 0x85, 'F23': 0x86, 'F24': 0x87,
              'NUMLOCK': 0x90, 'SCROLL': 0x91, 'LSHIFT': 0xA0, 'RSHIFT': 0xA1,
              'LCONTROL': 0xA2, 'RCONTROL': 0xA3, 'LMENU': 0xA4,
              'RMENU': 0xA5,'BROWSER_BACK': 0xA6, 'BROWSER_FORWARD': 0xA7,
              'BROWSER_REFRESH': 0xA8, 'BROWSER_STOP': 0xA9,
              'BROWSER_SEARCH': 0xAA, 'BROWSER_FAVORITES': 0xAB,
              'BROWSER_HOME': 0xAC, 'VOLUME_MUTE': 0xAD, 'VOLUME_DOWN': 0xAE,
              'VOLUME_UP': 0xAF, 'MEDIA_NEXT_TRACK': 0xB0,
              'MEDIA_PREV_TRACK': 0xB1, 'MEDIA_STOP': 0xB2,
              'MEDIA_PLAY_PAUSE': 0xB3, 'LAUNCH_MAIL': 0xB4,
              'LAUNCH_MEDIA_SELECT': 0xB5, 'LAUNCH_APP1': 0xB6,
              'LAUNCH_APP2': 0xB7, 'OEM_1': 0xBA, 'OEM_PLUS': 0xBB,
              'OEM_COMMA': 0xBC, 'OEM_MINUS': 0xBD, 'OEM_PERIOD': 0xBE,
              'OEM_2': 0xBF, 'OEM_3': 0xC0, 'OEM_4': 0xDB, 'OEM_5': 0xDC,
              'OEM_6': 0xDD, 'OEM_7': 0xDE, 'OEM_8': 0xDF, 'OEM_102': 0xE2,
              'PROCESSKEY': 0xE5, 'PACKET': 0xE7, 'ATTN': 0xF6, 'CRSEL': 0xF7,
              'EXSEL': 0xF8, 'EREOF': 0xF9, 'PLAY': 0xFA, 'ZOOM': 0xFB,
              'NONAME': 0xFC, 'PA1': 0xFD, 'OEM_CLEAR': 0xFE}


PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class KeyOutputer:
    def __init__(self):
        self.keys_down = set()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        for key in list(self.keys_down):
            self.key_up(key)
        self.keys_down.clear()

    def keyboard(self, dwFlags, key):
        hexKeyCode = KEY_MAP[key]
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, hexKeyCode, dwFlags, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

    def key_down(self, key):
        self.keys_down.add(key)
        self.keyboard(0x0008, key)

    def key_up(self, key):
        if key in self.keys_down:
            self.keys_down.remove(key)
        self.keyboard(0x0008 | 0x0002, key)

    def touch(self, key, delay=.01):
        self.key_down(key)
        sleep(delay)
        self.key_up(key)

    def type(self, keys, interval=.01, delay=.01):
        for key in keys:
            if key.isupper():
                self.key_down('LSHIFT')
                self.touch(key.lower(), delay)
                self.key_up('LSHIFT')
            elif key not in KEY_MAP:
                self.key_down('LSHIFT')
                self.touch(SHIFTED_KEY_MAP[key], delay)
                self.key_up('LSHIFT')
            else:
                self.touch(key, delay)
            sleep(interval)


class KeyCapturer(Capturer):
    def __init__(self):
        super().__init__()

    def capture(self):
        return {
            key: GetKeyState(code) for key, code in VK_KEY_MAP.items()
        }
