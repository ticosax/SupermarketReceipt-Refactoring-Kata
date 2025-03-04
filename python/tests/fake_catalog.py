from supermarket_receipt.catalog import SupermarketCatalog
from supermarket_receipt.model_objects import Product


class FakeCatalog(SupermarketCatalog):
    def __init__(self):
        self.prices = {}

    def add_product(self, product: Product, price: int):
        self.prices[product] = price

    def unit_price(self, product):
        return self.prices[product]
