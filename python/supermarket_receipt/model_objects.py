from dataclasses import dataclass
from enum import Enum


class ProductUnit(Enum):
    EACH = 1
    KILO = 2


@dataclass(frozen=True)
class Product:
    name: str
    unit: ProductUnit


@dataclass
class ProductQuantity:
    product: Product
    quantity: float


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4


@dataclass
class Offer:
    offer_type: SpecialOfferType
    product: Product
    argument: float


@dataclass
class Discount:
    product: Product
    description: str
    discount_amount: float
