# Excepciones personalizadas del sistema Software FJ


class ErrorSistema(Exception):
    """Excepcion base, todas las demas heredan de esta."""
    pass


class ClienteInvalidoError(ErrorSistema):
    """Datos del cliente incorrectos."""
    pass


class ServicioInvalidoError(ErrorSistema):
    """Servicio mal creado o que no existe."""
    pass


class ServicioNoDisponibleError(ErrorSistema):
    """El servicio esta desactivado o no hay unidades."""
    pass


class ReservaInvalidaError(ErrorSistema):
    """La reserva no cumple las condiciones."""
    pass


class OperacionNoPermitidaError(ErrorSistema):
    """Accion que no se puede hacer en el estado actual."""
    pass


class ParametroFaltanteError(ErrorSistema):
    """Falta un dato obligatorio."""
    pass


class CalculoInvalidoError(ErrorSistema):
    """El calculo del costo da un valor que no tiene sentido."""
    pass
