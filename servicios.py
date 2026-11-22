from abc import abstractmethod

from entidad import Entidad
from excepciones import (CalculoInvalidoError, ReservaInvalidaError,
                         ServicioInvalidoError, ServicioNoDisponibleError)

IVA = 0.19


class Servicio(Entidad):
    """Clase abstracta de la que heredan los tipos de servicio."""

    def __init__(self, nombre, precio):
        super().__init__()
        if not nombre:
            raise ServicioInvalidoError("El servicio necesita un nombre")
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ServicioInvalidoError(f"Precio invalido: {precio}")
        self.nombre = nombre
        self.precio = precio
        self.disponible = True

    @abstractmethod
    def costo_base(self, duracion):
        pass

    @abstractmethod
    def validar_duracion(self, duracion):
        pass

    def verificar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"{self.nombre} no esta disponible")

    # En Python no hay sobrecarga como en Java, asi que se simula con
    # parametros opcionales. Se puede llamar de tres formas:
    #   calcular_costo(duracion)
    #   calcular_costo(duracion, impuesto)
    #   calcular_costo(duracion, impuesto, descuento)
    def calcular_costo(self, duracion, impuesto=0, descuento=0):
        if not (0 <= impuesto <= 1):
            raise CalculoInvalidoError(f"Impuesto invalido: {impuesto}")
        if not (0 <= descuento <= 0.5):
            raise CalculoInvalidoError(f"Descuento no permitido: {descuento}")

        costo = self.costo_base(duracion)
        costo = costo - costo * descuento
        costo = costo + costo * impuesto

        if costo <= 0:
            raise CalculoInvalidoError(f"El costo dio {costo}, algo esta mal")
        return round(costo)

    def _revisar_rango(self, duracion, minimo, maximo):
        if not isinstance(duracion, (int, float)):
            raise ReservaInvalidaError(f"La duracion debe ser un numero, llego: {duracion}")
        if not (minimo <= duracion <= maximo):
            raise ReservaInvalidaError(
                f"Duracion {duracion} fuera del rango permitido ({minimo} a {maximo})")


class ReservaSala(Servicio):

    def __init__(self, nombre, precio, capacidad):
        super().__init__(nombre, precio)
        if capacidad <= 0:
            raise ServicioInvalidoError("La capacidad debe ser mayor a 0")
        self.capacidad = capacidad

    def validar_duracion(self, duracion):
        self._revisar_rango(duracion, 1, 8)  # horas

    def costo_base(self, duracion):
        return self.precio * duracion

    def mostrar_info(self):
        return f"Sala {self.id}: {self.nombre} ({self.capacidad} personas) ${self.precio}/hora"


class AlquilerEquipo(Servicio):

    def __init__(self, nombre, precio, unidades):
        super().__init__(nombre, precio)
        if unidades < 0:
            raise ServicioInvalidoError("Las unidades no pueden ser negativas")
        self.unidades = unidades

    def verificar_disponibilidad(self):
        super().verificar_disponibilidad()
        if self.unidades == 0:
            raise ServicioNoDisponibleError(f"No quedan unidades de {self.nombre}")

    def validar_duracion(self, duracion):
        self._revisar_rango(duracion, 1, 15)  # dias

    def costo_base(self, duracion):
        return self.precio * duracion

    def mostrar_info(self):
        return f"Equipo {self.id}: {self.nombre} ({self.unidades} unidades) ${self.precio}/dia"


class Asesoria(Servicio):

    recargos = {"basico": 1, "avanzado": 1.5, "experto": 2}

    def __init__(self, nombre, precio, nivel):
        super().__init__(nombre, precio)
        if nivel not in self.recargos:
            raise ServicioInvalidoError(f"Nivel de asesoria no valido: {nivel}")
        self.nivel = nivel

    def validar_duracion(self, duracion):
        self._revisar_rango(duracion, 1, 4)  # horas

    def costo_base(self, duracion):
        return self.precio * duracion * self.recargos[self.nivel]

    def mostrar_info(self):
        return f"Asesoria {self.id}: {self.nombre} (nivel {self.nivel}) ${self.precio}/hora"
