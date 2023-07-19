import math
from dataclasses import dataclass, field

from model_objects import Discount, Offer, Product, ProductQuantity, SpecialOfferType
from receipt import Receipt


@dataclass
class ShoppingCart:
    items: list[ProductQuantity] = field(default_factory=list)
    product_quantities: dict[Product, float] = field(default_factory=dict)

    def add_item(self, product: Product) -> None:
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        self.items.append(ProductQuantity(product, quantity))
        if product in self.product_quantities:
            self.product_quantities[product] = (
                self.product_quantities[product] + quantity
            )
        else:
            self.product_quantities[product] = quantity

    def handle_offers(self, receipt: Receipt, offers: dict[Product, Offer], catalog):
        for p, quantity in self.product_quantities.items():
            try:
                offer = offers[p]
            except KeyError:
                continue
            unit_price = catalog.unit_price(p)
            quantity_as_int = int(quantity)
            discount = None
            x = 1
            if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                x = 3

            elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                x = 2
                if quantity_as_int >= 2:
                    total = (
                        offer.argument * (quantity_as_int / x)
                        + quantity_as_int % 2 * unit_price
                    )
                    discount_n = unit_price * quantity - total
                    discount = Discount(p, "2 for " + str(offer.argument), -discount_n)

            if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                x = 5

            number_of_x = math.floor(quantity_as_int / x)
            if (
                offer.offer_type == SpecialOfferType.THREE_FOR_TWO
                and quantity_as_int > 2
            ):
                discount_amount = quantity * unit_price - (
                    (number_of_x * 2 * unit_price) + quantity_as_int % 3 * unit_price
                )
                discount = Discount(p, "3 for 2", -discount_amount)

            if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                discount = Discount(
                    p,
                    str(offer.argument) + "% off",
                    -quantity * unit_price * offer.argument / 100.0,
                )

            if (
                offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT
                and quantity_as_int >= 5
            ):
                discount_total = unit_price * quantity - (
                    offer.argument * number_of_x + quantity_as_int % 5 * unit_price
                )
                discount = Discount(
                    p, str(x) + " for " + str(offer.argument), -discount_total
                )

            if discount:
                receipt.add_discount(discount)
