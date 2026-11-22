from entidad import Entidad
from excepciones import (CalculoInvalidoError, OperacionNoPermitidaError,
                         ReservaInvalidaError)
from logger import logger
from servicios import IVA, AlquilerEquipo


class Reserva(Entidad):

    def __init__(self, cliente, servicio, duracion):
        super().__init__()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "pendiente"
        self.total = 0

    def confirmar(self):
        if self.estado != "pendiente":
            raise OperacionNoPermitidaError(f"La reserva {self.id} ya esta {self.estado}")
        try:
            self.servicio.verificar_disponibilidad()
            self.servicio.validar_duracion(self.duracion)
        except ReservaInvalidaError as e:
            # se encadena para no perder el error original
            raise ReservaInvalidaError(f"No se pudo confirmar la reserva {self.id}") from e
        else:
            # solo entra aqui si no hubo errores
            if isinstance(self.servicio, AlquilerEquipo):
                self.servicio.unidades -= 1
            self.estado = "confirmada"
            logger.info(f"Reserva {self.id} confirmada")

    def cancelar(self):
        if self.estado not in ("pendiente", "confirmada"):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar la reserva {self.id} porque esta {self.estado}")
        try:
            if self.estado == "confirmada" and isinstance(self.servicio, AlquilerEquipo):
                self.servicio.unidades += 1
            self.estado = "cancelada"
        finally:
            logger.info(f"Se intento cancelar la reserva {self.id}")

    def procesar(self, descuento=0):
        if self.estado != "confirmada":
            raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas")
        try:
            costo = self.servicio.calcular_costo(self.duracion, IVA, descuento)
        except CalculoInvalidoError as e:
            raise ReservaInvalidaError(f"Error al cobrar la reserva {self.id}") from e
        else:
            self.total = costo
            self.estado = "procesada"
            logger.info(f"Reserva {self.id} procesada por ${costo}")
        finally:
            logger.info(f"Fin del procesamiento de la reserva {self.id}")
        return self.total

    def mostrar_info(self):
        texto = f"Reserva {self.id}: {self.cliente.nombre} - {self.servicio.nombre} - {self.estado}"
        if self.total:
            texto += f" - ${self.total}"
        return texto
