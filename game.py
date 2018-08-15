import numpy as np
import time
import pyautogui
import order

class Game:

    def __init__(self, vision, controller, keyboard, clipboard):
        self.vision = vision
        self.controller = controller
        self.keyboard = keyboard
        self.clipboard = clipboard

        #self.state = 'not docked'

    def run(self):
        while True:
            self.vision.refresh_frame()
            time.sleep(1)
            if not self.in_station():
                self.log('Not In Station')
            elif not self.is_wallet_open():
                self.log('Wallet not open')
                self.open_wallet()
                time.sleep(4)

            if self.is_wallet_open():
                self.process_wallet_item()
            else:
                self.log('Not doing anything')

            time.sleep(1)

    def in_station(self):
        matches = self.vision.find_template('undock-button')
        return np.shape(matches)[1] >= 1

    def is_wallet_open(self):
        matches = self.vision.find_template('wallet-orders-selling-header')
        return np.shape(matches)[1] >= 1

    def open_wallet(self):
        self.keyboard.alt('w')

    def get_previous_list_item(self):
        self.keyboard.upArrow()
        time.sleep(0.2)
        self.keyboard.copy()
        return self.clipboard.get()

    def get_next_list_item(self):
        self.keyboard.downArrow()
        time.sleep(0.2)
        self.keyboard.copy()
        return self.clipboard.get()

    def get_next_wallet_order(self):
        return WalletOrder(self.get_next_list_item())

    def process_wallet_item(self):
        myWalletOrder = get_next_wallet_order()
        my_price = myWalletOrder.price()
        item_name =  myWalletOrder.itemName()
        time.sleep(0.5)
        self.vision.refresh_frame()

        if not self.move_to_selected_wallet_item_location():
            time.sleep(1.0)
            return

        time.sleep(0.2)
        pyautogui.doubleClick() # open order
        time.sleep(4.0)

        top_order = self.get_next_list_item()
        best_price = self.float_price(top_order)
        #print(top_order_items)
        result = "NEEDS UPDATE" if best_price < my_price else "ORDER ON TOP"
        print("%s: %.02f %.02f %s" % (item_name, my_price, best_price, result))

        if best_price < my_price and my_price - best_price < 5.00:
            new_best_price  = best_price - 0.01
            time.sleep(3)
            # todo skill price table
            self.vision.refresh_frame()

            if not self.move_to_my_order():
                self.open_wallet()
                time.sleep(2.0)
                return
            time.sleep(0.6)
            pyautogui.rightClick()
            time.sleep(1.0)
            pyautogui.moveRel(24,32, duration=0.2, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
            self.clipboard.put(new_best_price)
            time.sleep(0.5)
            self.keyboard.paste()
            time.sleep(0.3)
            self.keyboard.returnKey()
        self.open_wallet()
        time.sleep(2.0)

    def move_to_modify_order_context_menu_item(self):
        pyautogui.moveTo(x + 20, y + 25, duration=0.3, tween=pyautogui.easeInOutQuad)


    def move_to_my_order(self):
        matches = self.vision.find_template('my-order-highlight', threshold=0.95)

        if np.shape(matches)[1] >= 1:
            x = matches[1][0]
            y = matches[0][0]
            pyautogui.moveTo(x + 20, y, duration=0.3, tween=pyautogui.easeInOutQuad)
            return True
        else:
            return False

    def move_to_selected_wallet_item_location(self):
        matches = self.vision.find_template('selected-wallet-order', threshold=0.9)

        if np.shape(matches)[1] >= 1:
            x = matches[1][0]
            y = matches[0][0]
            pyautogui.moveTo(x - 30, y + 10, duration=0.3, tween=pyautogui.easeInOutQuad)  # use tweening/easing function to move mouse over 2 seconds.
            return True
        else:
            return False

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
