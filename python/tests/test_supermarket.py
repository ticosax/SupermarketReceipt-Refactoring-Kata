from supermarket_receipt.model_objects import Discount, SpecialOfferType
from supermarket_receipt.shopping_cart import ShoppingCart
from supermarket_receipt.teller import Teller


def test_ten_percent_discount(catalog, apples):
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apples, 10.0)

    cart = ShoppingCart()
    cart.add_item_quantity(apples, 2.5)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == 447.75
    assert receipt.discounts == [Discount(apples, "10.0% off", -49.75)]
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == apples
    assert receipt_item.price == 199
    assert receipt_item.total_price == 199 * 2.5
    assert receipt_item.quantity == 2.5


def test_3_for_2_discount(catalog, toothbrush):
    teller = Teller(catalog)
    teller.add_special_offer(
        SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.unit_price(toothbrush)
    )
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 4)
    receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == 99 * 3
    assert receipt.discounts == [Discount(toothbrush, "3 for 2", -99)]
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == toothbrush
    assert receipt_item.price == 99
    assert receipt_item.total_price == 99 * 4
    assert receipt_item.quantity == 4


def test_5_for_amount_discount(catalog, toothbrush):
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothbrush, 400)
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 6)
    receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == 400 + 99
    assert receipt.discounts == [Discount(toothbrush, "5 for 400", -95)]
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == toothbrush
    assert receipt_item.price == 99
    assert receipt_item.total_price == 594
    assert receipt_item.quantity == 6


def test_2_for_amount_discount(catalog, toothbrush):
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 150)
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)
    receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == 150
    assert receipt.discounts == [Discount(toothbrush, "2 for 150", -48)]
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == toothbrush
    assert receipt_item.price == 99
    assert receipt_item.total_price == 198
    assert receipt_item.quantity == 2


def test_2_for_amount_discount_2_times(catalog, toothbrush):
    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothbrush, 150)
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 4)
    receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == 300
    assert receipt.discounts == [
        Discount(toothbrush, "2 for 150", -96),
    ]
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == toothbrush
    assert receipt_item.price == 99
    assert receipt_item.total_price == 396
    assert receipt_item.quantity == 4


def test_shopping_cart_no_matching_discount(catalog, apples, toothbrush):
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


def test_shopping_cart_add_item(catalog, toothbrush):
    teller = Teller(catalog)

    cart = ShoppingCart()
    cart.add_item(toothbrush)

    receipt = teller.checks_out_articles_from(cart)

    assert receipt.total_price() == 99
    assert receipt.discounts == []
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == toothbrush
    assert receipt_item.price == 99
    assert receipt_item.total_price == 99
    assert receipt_item.quantity == 1


def test_3_for_2_discount_less_than_3(catalog, toothbrush):
    teller = Teller(catalog)
    teller.add_special_offer(
        SpecialOfferType.THREE_FOR_TWO, toothbrush, catalog.unit_price(toothbrush)
    )
    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 2)
    receipt = teller.checks_out_articles_from(cart)
    assert receipt.total_price() == 99 * 2
    assert receipt.discounts == []
    assert len(receipt.items) == 1
    receipt_item = receipt.items[0]
    assert receipt_item.product == toothbrush
    assert receipt_item.price == 99
    assert receipt_item.total_price == 99 * 2
    assert receipt_item.quantity == 2
