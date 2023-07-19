from model_objects import SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller


def test_ten_percent_discount(catalog, toothbrush, apples):
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == 497.5
    assert receipt.discounts == []
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == apples
    assert receipt_item.price == 199
    assert receipt_item.total_price == 199 * 2.5
    assert receipt_item.quantity == 2.5
