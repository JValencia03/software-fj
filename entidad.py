from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta para todo lo que se guarda en el sistema."""

    contador = 0

    def __init__(self):
        Entidad.contador += 1
        self._id = Entidad.contador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def mostrar_info(self):
        pass

    def __str__(self):
        return self.mostrar_info()
