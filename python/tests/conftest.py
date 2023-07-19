import pytest
from receipt import Receipt
from model_objects import Product, ProductUnit, Discount
from tests.fake_catalog import FakeCatalog


@pytest.fixture()
def catalog() -> FakeCatalog:
    return FakeCatalog()


@pytest.fixture()
def apples(catalog) -> Product:
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 1.99)
    return apples


@pytest.fixture()
def baguette(catalog) -> Product:
    baguette = Product("baguette", ProductUnit.EACH)
    catalog.add_product(baguette, 1.3)
    return baguette


@pytest.fixture()
def toothbrush(catalog) -> Product:
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)
    return toothbrush


@pytest.fixture()
def no_discount_receipt(apples, baguette) -> Receipt:
    receipt = Receipt()
    receipt.add_product(apples, 2, 0.9, 2 * 0.9)
    receipt.add_product(baguette, 3, 1.3, 3 * 1.3)
    return receipt


@pytest.fixture()
def percent_discount_receipt(apples, baguette) -> Receipt:
    receipt = Receipt()
    receipt.add_product(apples, 2, 0.9, 2 * 0.9)
    receipt.add_product(baguette, 3, 1.3, 3 * 1.3)
    discount = Discount(baguette, "10% discount", -(3*1.13*0.1))
    receipt.add_discount(discount)
    return receipt
