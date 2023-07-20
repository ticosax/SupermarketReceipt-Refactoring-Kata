import mimetypes
from functools import partial

from jinja2 import Environment, PackageLoader, select_autoescape

from supermarket_receipt.model_objects import Discount, ProductUnit
from supermarket_receipt.receipt import Receipt, ReceiptItem


def render_item_line(columns: int, item: ReceiptItem):
    line_price = f"{item.total_price/ 100:.2f}"
    blank_space = " " * (columns - len(line_price) - len(item.product.name))
    return f"{item.product.name}{blank_space}{line_price}"


def render_total_line(columns: int, receipt: Receipt):
    line_price = f"{receipt.total_price () / 100:.2f}"
    blank_space = " " * (columns - len(line_price) - 6)
    return f"Total:{blank_space}{line_price}"


def render_discount_line(columns: int, discount: Discount):
    lhs = f"{discount.description} ({discount.product.name})"
    line_discount_amount = f"{discount.discount_amount / 100:.2f}"
    blank_space = " " * (columns - len(line_discount_amount) - len(lhs))
    return f"{lhs}{blank_space}{line_discount_amount}"


def is_each(unit: ProductUnit) -> bool:
    return unit is ProductUnit.EACH


class ReceiptPrinter:
    def __init__(self, columns=40):
        self.columns = columns

    def print_receipt(self, receipt: Receipt, mimetype: str = "text/plain"):
        env = Environment(
            loader=PackageLoader("supermarket_receipt"), autoescape=select_autoescape()
        )
        env.filters["asitemline"] = partial(render_item_line, self.columns)
        env.filters["astotalline"] = partial(render_total_line, self.columns)
        env.filters["asdiscountline"] = partial(render_discount_line, self.columns)
        env.filters["is_each"] = is_each
        extension = mimetypes.guess_extension(mimetype)
        template = env.get_template(f"receipt{extension}")
        return template.render(receipt=receipt, columns=self.columns)
