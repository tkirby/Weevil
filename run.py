import cv2
import numpy as np

from vision import Vision
from controller import Controller
from keyboard import Keyboard
from clipboard import Clipboard

from game import Game

vision = Vision()
controller = Controller()
keyboard = Keyboard()
clipboard = Clipboard()
game = Game(vision, controller, keyboard, clipboard)

from pynput.keyboard import Key, Listener
#defining function to print when key is pressed
def on_press(key):
    pass
  #print('{0} pressed'.format(key))
#defining function to print when key is released
def on_release(key):
  #print('{0} release'.format(key))
  if key == Key.esc:
    # Stop listener
    return False
    if key == Key.shift:
        if game.state == "paused":
            game.state = "started"
        else:
            game.state = "paused"

# Collect events until released
with Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    game.run()
    listener.join()
