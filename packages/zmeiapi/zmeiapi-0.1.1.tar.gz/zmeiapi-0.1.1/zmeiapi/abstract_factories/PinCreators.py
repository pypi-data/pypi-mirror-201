__version__ = "0.1.1"
__author__ = 'Vlad Romanenko'


from abc import ABC, abstractmethod
from zmeiapi.zmei_io.Logger import logger


class PinCreator(ABC):
    @abstractmethod
    def __init__(self, number, layer_number, materials, radiuses):
        self.number = number
        self.layer_number = layer_number
        self.materials = materials
        self.radiuses = radiuses
        if len(self.materials) - len(self.radiuses) != 1:
            raise AttributeError("The lenghs of materials and radiuses listsare wrong")

    @abstractmethod
    def create_pin(
            self,
            name: str,
            **kwargs
    ):
        pass


class NumberedPinsCreator(ABC):
    @abstractmethod
    def __init__(self, number, materials, radiuses):
        self.number = number
        self.materials = materials
        self.radiuses = radiuses
        if len(self.materials) - len(self.radiuses) != 1:
            raise AttributeError("The lenghs of materials and radiuses listsare wrong")

    @abstractmethod
    def create_pins(
            self,
            name: str,
            **kwargs
    ):
        pass


class CorePinsCreator(ABC):
    @abstractmethod
    def __init__(self, fas_amount, layers_amount, materials, radiuses):
        self.fas_amount = fas_amount
        self.layers_amount = layers_amount
        self.materials = materials
        self.radiuses = radiuses
        if len(self.materials) - len(self.radiuses) != 1:
            raise AttributeError("The lenghs of materials and radiuses listsare wrong")

    @abstractmethod
    def create_pins(
            self,
            name: str,
            **kwargs
    ):
        pass
