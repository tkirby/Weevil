
class Order(object):
    def __init__(self, string):
        self.orderString = string
        self.items = self.orderString.split('\t')
        if len(self.items) < 3:
            raise ValueError('Couldn\'t parse order string')
        isk_price = self.items[2].split()
        price_string = filter(lambda char: char not in ",", isk_price[0])
        self.price = float(price_string)

class WalletOrder(Order):
    def __init__(self, string):
        super(WalletOrder, self).__init__(string)
        self.itemName = self.items[0]

    def __eq__(self, other):
        return self.itemName == other.itemName and self.price == other.price
