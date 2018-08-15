import pyautogui

class Keyboard:
    def __init__(self):
        pass

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
