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

# screenshot = vision.get_image('tests/screens/round-finished-results.png')
# print(screenshot)
# match = vision.find_template('bison-head', image=screenshot)
# print(np.shape(match)[1])

game.run()
