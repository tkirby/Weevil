import csv

class SkillBook(object):
    def __init__(self):
        with open('data\skillbook_npc_prices.csv', mode='r') as infile:
            reader = csv.reader(infile)
            self.price_list = {rows[0]:rows[1] for rows in reader}
            #print(self.price_list)

    def npc_price(self, string):
        if string in self.price_list:
            return float(self.price_list[string])
        else:
            return None
