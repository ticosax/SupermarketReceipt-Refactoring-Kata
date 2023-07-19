from abc import ABC, abstractmethod

from model_objects import Product

NOT_IMPLEMENTED_MESSAGE = "cannot be called from a unit test - it accesses the database"


class SupermarketCatalog(ABC):
    @abstractmethod
    def add_product(self, product: Product, price: int):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)

    @abstractmethod
    def unit_price(self, product: Product):
        raise NotImplementedError(NOT_IMPLEMENTED_MESSAGE)
