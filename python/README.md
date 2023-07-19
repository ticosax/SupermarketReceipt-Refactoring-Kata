# Supermarket Receipt in [Python](https://www.python.org/)

## Setup

* Have Python installed
* Clone the repository
* On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory
* On the command line, install requirements, e.g. on the`python -m pip install -r requirements.txt`

## Running Tests

On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory and run

```
pytest
```

## Optional: Running [TextTest](https://www.texttest.org/) Tests

Install TextTest according to the [instructions](https://www.texttest.org/index.html#getting-started-with-texttest) (platform specific).

On the command line, enter the `SupermarketReceipt-Refactoring-Kata/python` directory and run

```
texttest -a sr -d .
```

## My notes:

- Switch to poetry to deal with dependencies and virtualen environment.
- Measure coverage to find out which part of the project must be tested

    ---------- coverage: platform linux, python 3.11.3-final-0 -----------
    Name                        Stmts   Miss  Cover
    -----------------------------------------------
    catalog.py                      5      2    60%
    model_objects.py               27      3    89%
    receipt.py                     27      2    93%
    receipt_printer.py             44     44     0%
    shopping_cart.py               49     29    41%
    teller.py                      19      0   100%
    tests/__init__.py               0      0   100%
    tests/fake_catalog.py          10      0   100%
    tests/test_supermarket.py      24      0   100%
    -----------------------------------------------
    TOTAL                         205     80    61%

    Looks like, I will focus on the printer, shopping cart and catalog modules
- Dealing with currency as floats can lead to rounding errors,
we should convert everything to integer (For our use case, the unit will be cents.),
and delegate the conversion to Currency units to the presentation layer.
- Adopt a code formatting tool such as black.
- Adopt a linter such as ruff.
- I see a lot of bare classes where dataclass or maybe pydantic would help to keep the code more data focused.
- Typing annotations would help and increase quality of the code and make the refactoring less error prone.


### Catalog.py 
- I would not raise bare exception, NotImplementedError looks like a better fit.

### teller.py 
- The class Teller receives a catalog instance as init arg. This looks like a code smell. If keeping references to a external objects is not necessary, it should be avoided as it can defeat garbage collection it the Telle outlive the Catalog.

### model_objects.py 
- convert to dataclasses or pydantic models (pydantic if serialization would be proved to be useful later.)

### receipt.py 
- ReceiptItem -> convert to dataclass
- Receipt -> Makes inner _items and _discounts private for no particular reason (except ReceiptItem remains private and hidden). Not sure it will stay.

### receipt_printer.py 
- Looks like the whole thing, would be better implemented with a template engine.
- At first glance, I would choose to convert the Receipt into a intermediary representation format such as json or xml. That, in turn, would be transformed into one of multiple output. we could then have a serializer for plain text, html, pdf, ods, xml, ... The specific choice about which transformation stack that should be used, depends on the use case. XML + XSLT related stack offers a wide variety of choices to transform the receipt into many formats. For the sake of this kata excercise, [jinja](https://jinja.palletsprojects.com/en/3.1.x/) would probably be a good fit. 

### shopping_cart.py 

- Lot of tiny refactoring looks necessary
- iteration over dict.keys() instead of dict.items()
- a big if/elif/else block would be probably better as rewritten with a match/case expression.
-  Discount.description could be refactored, to leave the presentation concerns out of it.
