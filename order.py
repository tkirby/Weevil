
class Order:
    def __init__(self, string):
        self.orderString = string
        self.items = self.orderString.split('\t')
        isk_price = items[2].split()
        price_string = filter(lambda char: char not in ",", isk_price[0])
        self.price = float(price_string)
        
class WalletOrder(Order):
    def __init__(self, string):
        self.itemName = self.items[0]
