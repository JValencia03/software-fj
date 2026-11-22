from cliente import Cliente
from excepciones import (ClienteInvalidoError, ErrorSistema,
                         OperacionNoPermitidaError, ParametroFaltanteError,
                         ReservaInvalidaError, ServicioInvalidoError)
from logger import logger
from reserva import Reserva


class SistemaReservas:
    """Guarda todo en listas, no se usa base de datos."""

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, datos):
        try:
            cliente = Cliente(**datos)
        except TypeError as e:
            # pasa cuando falta un dato en el diccionario
            raise ParametroFaltanteError("Faltan datos para registrar el cliente") from e

        for c in self.clientes:
            if c.documento == cliente.documento:
                raise OperacionNoPermitidaError(f"El documento {cliente.documento} ya existe")

        self.clientes.append(cliente)
        logger.info(f"Cliente registrado: {cliente.nombre}")
        return cliente

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        logger.info(f"Servicio agregado: {servicio.nombre}")
        return servicio

    def buscar_cliente(self, documento):
        for c in self.clientes:
            if c.documento == documento:
                return c
        raise ClienteInvalidoError(f"No hay cliente con documento {documento}")

    def buscar_servicio(self, nombre):
        for s in self.servicios:
            if s.nombre == nombre:
                return s
        raise ServicioInvalidoError(f"No existe el servicio {nombre}")

    def hacer_reserva(self, documento, nombre_servicio, duracion, descuento=0):
        """Crea, confirma y procesa una reserva. Si algo falla la cancela."""
        try:
            cliente = self.buscar_cliente(documento)
            servicio = self.buscar_servicio(nombre_servicio)
        except ErrorSistema as e:
            raise ReservaInvalidaError("No se pudo crear la reserva") from e

        reserva = Reserva(cliente, servicio, duracion)
        self.reservas.append(reserva)
        try:
            reserva.confirmar()
            reserva.procesar(descuento)
        except ErrorSistema:
            reserva.cancelar()
            raise
        return reserva
