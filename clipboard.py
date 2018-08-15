from Tkinter import Tk
import pyperclip

class Clipboard:
    def __init__(self):
        pass

    def get(self):
        return Tk().clipboard_get()

    def put(self, string):
        pyperclip.copy(string)
