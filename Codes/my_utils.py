import win32gui
from win32gui import FindWindow, GetWindowRect
import ctypes
from ctypes import *

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print ("\n--------",hex(hwnd), win32gui.GetWindowText( hwnd ))

win32gui.EnumWindows( winEnumHandler, None )


def get_reso(name):
    window_handle = FindWindow(None, name)
    window_rect   = GetWindowRect(window_handle)
    return window_rect




''''
def GetWindowRectFromName(name:str)-> tuple:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    # print(hwnd)
    # print(rect)
    return (rect.left, rect.top, rect.right, rect.bottom)

print(GetWindowRectFromName("Command Prompt"))'''