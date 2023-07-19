import pytest

from supermarket_receipt.model_objects import Discount, Product, ProductUnit
from supermarket_receipt.receipt import Receipt
from tests.fake_catalog import FakeCatalog


@pytest.fixture()
def catalog() -> FakeCatalog:
    return FakeCatalog()


@pytest.fixture()
def apples(catalog) -> Product:
    apples = Product("apples", ProductUnit.KILO)
    catalog.add_product(apples, 199)
    return apples


@pytest.fixture()
def baguette(catalog) -> Product:
    baguette = Product("baguette", ProductUnit.EACH)
    catalog.add_product(baguette, 13)
    return baguette


@pytest.fixture()
def toothbrush(catalog) -> Product:
    toothbrush = Product("toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 99)
    return toothbrush


@pytest.fixture()
def cloves_the_spice(catalog) -> Product:
    cloves = Product("cloves", ProductUnit.KILO)
    catalog.add_product(cloves, 1000)
    return cloves


@pytest.fixture()
def cloves_the_hardware(catalog) -> Product:
    cloves = Product("cloves", ProductUnit.EACH)
    catalog.add_product(cloves, 10)
    return cloves


@pytest.fixture()
def no_discount_receipt(apples, baguette) -> Receipt:
    receipt = Receipt()
    receipt.add_product(apples, 2, 90, 2 * 90)
    receipt.add_product(baguette, 3, 130, 3 * 130)
    return receipt


@pytest.fixture()
def percent_discount_receipt(apples, baguette) -> Receipt:
    receipt = Receipt()
    receipt.add_product(apples, 2, 90, 2 * 90)
    receipt.add_product(baguette, 3, 130, 3 * 130)
    discount = Discount(baguette, "10% discount", -(3 * 130 * 0.1))
    receipt.add_discount(discount)
    return receipt


@pytest.fixture()
def bulk_discount_receipt(apples, baguette) -> Receipt:
    receipt = Receipt()
    receipt.add_product(baguette, 3, 130, 3 * 130)
    receipt.add_product(apples, 2, 90, 2 * 90)
    discount = Discount(baguette, "3 for 2", -130)
    receipt.add_discount(discount)
    return receipt
