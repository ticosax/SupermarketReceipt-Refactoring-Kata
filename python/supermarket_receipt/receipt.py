from dataclasses import dataclass, field
from math import fsum

from supermarket_receipt.model_objects import Discount, Product


@dataclass
class ReceiptItem:
    product: Product
    quantity: float
    price: float
    total_price: float


@dataclass
class Receipt:
    items: list[ReceiptItem] = field(default_factory=list)
    discounts: list[Discount] = field(default_factory=list)

    def total_price(self):
        total = fsum(item.total_price for item in self.items)
        total += fsum(discount.discount_amount for discount in self.discounts)
        return total

    def add_product(self, product, quantity, price, total_price):
        self.items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        self.discounts.append(discount)
