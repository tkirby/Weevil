import pyautogui
import ctypes

class Keyboard:
    def __init__(self):
        self.keyboardDLL = ctypes.windll.user32

    def ctrlShift(self, key):
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('shift')
        pyautogui.typewrite([key])
        pyautogui.keyUp('shift')
        pyautogui.keyUp('ctrl')

    def alt(self, key):
        pyautogui.keyDown('alt')
        pyautogui.typewrite([key])
        pyautogui.keyUp('alt')

    def downArrow(self):
        pyautogui.typewrite(['down'])

    def upArrow(self):
        pyautogui.typewrite(['up'])

    def copy(self):
        pyautogui.keyDown('ctrl')
        pyautogui.typewrite(['c'])
        pyautogui.keyUp('ctrl')

    def paste(self):
        pyautogui.keyDown('ctrl')
        pyautogui.typewrite(['v'])
        pyautogui.keyUp('ctrl')

    def returnKey(selr):
        pyautogui.typewrite(['return'])

    def capsLockDown(self):
        VK_CAPITAL = 0x14
        return self.keyboardDLL.GetKeyState(VK_CAPITAL) & 1
