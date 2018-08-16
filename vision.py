import cv2
#import mss.tools
import mss

from PIL import Image
import numpy as np
import time
from collections import namedtuple

Point = namedtuple("Point", "x y")

#ssnumber = 1

class Vision:
    def __init__(self):
        self.static_templates = {
            'undock-button': 'assets/undock_button.png',
            'wallet-orders-selling-header': 'assets/wallet_orders_selling_header.png',
            'selected-wallet-order': 'assets/selected_wallet_order.png',
            'my-order-highlight' : 'assets/my_order_highlight.png',
            'modify-order-context-menu-item' : 'assets/modify_order_context_menu_item.png',
            'market-sellers-heading' : 'assets/market_sellers_heading.png'
        }

        self.templates = { k: cv2.imread(v, 0) for (k, v) in self.static_templates.items() }

        self.monitor = {'top': 0, 'left': 0, 'width': 1360, 'height': 768}
        self.screen = mss.mss()

        self.frame = None

    def take_screenshot(self):
        sct_img = mss.mss().grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #mss.tools.to_png(sct_img.rgb, sct_img.size, output="debug-%d.png" % ssnumber)
        #ssnumber = ssnumber + 1
        return img_gray

    def matching_algo(self, r, g, b, r_query, g_query, b_query):
        if r == r_query and g == g_query and b == b_query:
            return True
        else:
            return False


    def find_rgb(self, r_query, g_query, b_query, start_offset=None, end_offset=None):
        img = mss.mss().grab(self.monitor)
        pix = Image.frombytes('RGB', img.size, img.rgb)
        x_min = start_offset[0] if start_offset is not None else 0
        y_min = start_offset[1] if start_offset is not None else 0
        x_max = end_offset[0] if end_offset is not None else img.size[0]
        y_max = end_offset[1] if end_offset is not None else img.size[1]
        for x in range(x_min, x_max):
            for y in range(y_min, y_max):
                r, g, b = pix.getpixel((x,y))
                #print(r, g, b)
                if self.matching_algo(r, g, b, r_query, g_query, b_query):
                    #print(x, y)
                    # print("{},{} contains {}-{}-{} ".format(x, y, r, g, b))
                    return Point(x=x, y=y)
        return None

    def get_image(self, path):
        return cv2.imread(path, 0)

    def bgr_to_rgb(self, img):
        b,g,r = cv2.split(img)
        return cv2.merge([r,g,b])

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def match_template(self, img_grayscale, template, threshold=0.9):
        """
        Matches template image in a target grayscaled image
        """

        res = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    def find_image(self, name, image=None, threshold=0.9):
        matches = self.find_template(name, image, threshold)

        if np.shape(matches)[1] >= 1:
            x = matches[1][0]
            y = matches[0][0]
            return Point(x=x, y=y)
        else:
            return None

    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        initial_template = self.templates[name]
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
            matches = self.match_template(
                image,
                scaled_template,
                threshold
            )
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def refresh_frame(self):
        self.frame = self.take_screenshot()
