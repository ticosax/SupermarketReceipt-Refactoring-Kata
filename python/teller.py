from dataclasses import dataclass, field
from typing import TypeAlias

from catalog import SupermarketCatalog
from model_objects import Offer, Product, SpecialOfferType
from receipt import Receipt
from shopping_cart import ShoppingCart

Offers: TypeAlias = dict[Product, Offer]


@dataclass
class Teller:
    catalog: SupermarketCatalog
    offers: Offers = field(default_factory=dict)

    def add_special_offer(
        self, offer_type: SpecialOfferType, product: Product, argument: float
    ) -> None:
        self.offers[product] = Offer(offer_type, product, argument)

    def checks_out_articles_from(self, the_cart: ShoppingCart) -> Receipt:
        receipt = Receipt()
        product_quantities = the_cart.items
        for pq in product_quantities:
            p = pq.product
            quantity = pq.quantity
            unit_price = self.catalog.unit_price(p)
            price = quantity * unit_price
            receipt.add_product(p, quantity, unit_price, price)

        the_cart.handle_offers(receipt, self.offers, self.catalog)

        return receipt
