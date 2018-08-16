import numpy as np
import time
import pyautogui
from random import randint
from order import Order, WalletOrder
from skillbook import SkillBook

class Game:

    def __init__(self, vision, controller, keyboard, clipboard):
        self.vision = vision
        self.controller = controller
        self.keyboard = keyboard
        self.clipboard = clipboard
        self.state = "startup"
        self.top_order_location = None
        self.skillbooks = SkillBook()
        self.previous_wallet_order = None

    def delay(self, delay):
        multiplyer = 3.0 if self.state == "startup" else 1.0
        time.sleep(delay * multiplyer)

    def run(self):
        while True:
            self.vision.refresh_frame()
            if self.keyboard.capsLockDown():
                print("Paused")
                self.top_order_location = None # Reset since we might have moved windows while paused
                self.delay(1)
            else:
                if self.is_wallet_open():
                    self.process_wallet_item()
                else:
                    self.log('Not doing anything')
                    self.delay(1)

    def in_station(self):
        return self.vision.find_image('undock-button') is not None

    def is_wallet_open(self):
        return self.vision.find_image('wallet-orders-selling-header') is not None

    def open_wallet(self):
        self.keyboard.alt('w')

    def get_previous_list_item(self):
        self.keyboard.upArrow()
        self.delay(0.2)
        self.keyboard.copy()
        return self.clipboard.get()

    def get_next_list_item(self):
        self.keyboard.downArrow()
        self.delay(0.2)
        self.keyboard.copy()
        return self.clipboard.get()

    def get_next_wallet_order(self):
        listString = self.get_next_list_item()
        if listString == "":
            return None
        return WalletOrder(listString)

    def get_next_market_order(self):
        listString = self.get_next_list_item()
        if listString == "":
            return None
        return Order(listString)

    def process_wallet_item(self):
        myWalletOrder = None
        try:
            myWalletOrder = self.get_next_wallet_order()
        except:
            return

        #if self.previous_wallet_order != None and \
         #myWalletOrder == self.previous_wallet_order:
        #    print("Last item")
        #    self.open_wallet() # this will close if already open so we can start over
        #    return

        self.vision.refresh_frame()

        if not self.move_to_selected_wallet_item_location():
            self.delay(1.0) # give wallet time to update
            return

        pyautogui.doubleClick() # open order
        self.delay(1.0) # wait for market window to open
        self.process_order(myWalletOrder)
        self.open_wallet() # # move back to wallet

    def should_update(self, walletOrder, toPrice):
        if toPrice > walletOrder.price:
            return False

        npc_price = self.skillbooks.npc_price(walletOrder.itemName)
        if npc_price is not None:
            profit_percent = (toPrice - npc_price) / npc_price
            if npc_price >= 999999 and profit_percent > 0.15:
                return True
            elif npc_price < 999999 and profit_percent > 0.60:
                return True
        elif walletOrder.price - toPrice < 25.00: # TODO Percent
            return True

        return False

    def process_order(self, walletOrder):
        if self.we_are_top_order():
            print("We are top order")
            return

        top_order = None
        try :
            top_order = self.get_next_market_order()
        except:
            print("Failed to get top order")
            return

        new_best_price = top_order.price - 0.01
        if self.should_update(walletOrder=walletOrder, toPrice=new_best_price):

            if self.update_order(toPrice=new_best_price):
                self.state = "loaded" # we can go faster after everything has loaded
            else:
                print("Could not update order")

    def update_order(self, toPrice):

        self.vision.refresh_frame()
        self.delay(0.5)

        if not self.move_to_my_order():
            return False
        self.delay(0.4)
        pyautogui.rightClick()
        self.delay(0.3)
        pyautogui.moveRel(24,32, duration=0.2, tween=pyautogui.easeInOutQuad)
        pyautogui.click()
        self.clipboard.put(toPrice)
        self.delay(0.5)
        self.keyboard.paste()
        self.delay(0.3)
        self.keyboard.returnKey()

        # close any dialogs that pop up.
        self.delay(0.2)
        self.keyboard.returnKey()
        return True

    def move_to_modify_order_context_menu_item(self):
        pyautogui.moveTo(x + 20, y + 25, duration=0.3, tween=pyautogui.easeInOutQuad)

    def top_order_loc(self):
        if self.top_order_location == None: # TODO: USe offset to look this up periodically in caes it is moved
            header_location = self.find_market_header_location()
            if header_location is not None:
                self.top_order_location = (header_location.x + 65, header_location.y + 55)

        return self.top_order_location

    def we_are_top_order(self):
        top_loc = self.top_order_loc()
        if top_loc == None:
            return False
        end_offset = (top_loc[0] + 1, top_loc[1] + 1)
        offset = self.vision.find_rgb(27, 28, 92, start_offset=top_loc, end_offset=end_offset)
        return offset is not None

    def find_market_header_location(self):
        return self.vision.find_image('market-sellers-heading', threshold=0.9)

    def move_to_my_order(self):
        #matches = self.vision.find_template('my-order-highlight', threshold=0.95)
        top_loc = self.top_order_loc()

        loc = self.vision.find_rgb(27, 28, 92, start_offset=top_loc)
        if loc == None:
            return False

        #print(loc.x, loc.y)

        rand_x = randint(0,100)
        rand_y = randint(0,5)
        pyautogui.moveTo(loc.x + 15 + rand_x, loc.y + 15 + rand_y, duration=0.3, tween=pyautogui.easeInOutQuad)

        return True

    def move_to_selected_wallet_item_location(self):
        loc = self.vision.find_image('selected-wallet-order', threshold=0.9)

        if loc is not None:
            rand_x = randint(0,100)
            rand_y = randint(0,4)
            pyautogui.moveTo(loc.x - 30 - rand_x, loc.y + 10 + rand_y, duration=0.3, tween=pyautogui.easeInOutQuad)  # use tweening/easing function to move mouse over 2 seconds.
            return True
        else:
            return False

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
