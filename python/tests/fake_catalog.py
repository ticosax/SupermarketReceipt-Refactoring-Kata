from catalog import SupermarketCatalog


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.prices = {}

    def add_product(self, product, price):
        self.prices[product] = price

    def unit_price(self, product):
        return self.prices[product]
