import math
from dataclasses import dataclass, field

from supermarket_receipt.model_objects import (
    Discount,
    Offer,
    Product,
    ProductQuantity,
    SpecialOfferType,
)
from supermarket_receipt.receipt import Receipt


def _n_for_amount(
    x: int,
    product: Product,
    quantity: float,
    offer: Offer,
    unit_price: int,
    quantity_as_int: int,
) -> Discount:
    number_of_x = math.floor(quantity_as_int / x)
    total = offer.argument * number_of_x + quantity_as_int % x * unit_price
    discount_n = unit_price * quantity - total
    return Discount(product, f"{x} for {offer.argument}", -discount_n)


def _discount_builder(
    product: Product,
    quantity: float,
    offer: Offer,
    unit_price: int,
    quantity_as_int: int,
) -> Discount | None:
    match offer.offer_type:
        case SpecialOfferType.TWO_FOR_AMOUNT if quantity_as_int >= 2:
            return _n_for_amount(
                2, product, quantity, offer, unit_price, quantity_as_int
            )
        case SpecialOfferType.FIVE_FOR_AMOUNT if quantity_as_int >= 5:
            return _n_for_amount(
                5, product, quantity, offer, unit_price, quantity_as_int
            )
        case SpecialOfferType.THREE_FOR_TWO if quantity_as_int >= 3:
            x = 3
            number_of_x = math.floor(quantity_as_int / x)
            discount_amount = quantity * unit_price - (
                (number_of_x * 2 * unit_price) + quantity_as_int % x * unit_price
            )
            return Discount(product, "3 for 2", -discount_amount)
        case SpecialOfferType.TEN_PERCENT_DISCOUNT:
            return Discount(
                product,
                str(offer.argument) + "% off",
                -quantity * unit_price * offer.argument / 100.0,
            )
        case _:
            message = f"Kind of offer not handled {offer.offer_type}"
            raise NotImplementedError(message)


@dataclass
class ShoppingCart:
    items: list[ProductQuantity] = field(default_factory=list)
    product_quantities: dict[Product, list[float]] = field(default_factory=dict)

    def add_item(self, product: Product) -> None:
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product: Product, quantity: float) -> None:
        self.items.append(ProductQuantity(product, quantity))
        self.product_quantities.setdefault(product, []).append(quantity)

    def handle_offers(self, receipt: Receipt, offers: dict[Product, Offer], catalog):
        for (
            p,
            quantities,
        ) in self.product_quantities.items():
            try:
                offer = offers[p]
            except KeyError:
                continue
            unit_price = catalog.unit_price(p)
            quantity = math.fsum(quantities)
            quantity_as_int = int(quantity)
            if discount := _discount_builder(
                p, quantity, offer, unit_price, quantity_as_int
            ):
                receipt.add_discount(discount)
