from excepciones import ErrorSistema
from logger import logger
from servicios import AlquilerEquipo, Asesoria, ReservaSala
from sistema import SistemaReservas

sistema = SistemaReservas()
exitosas = 0
fallidas = 0


def ejecutar(numero, descripcion, operacion):
    """Ejecuta una operacion sin dejar que el programa se caiga."""
    global exitosas, fallidas
    print(f"\n{numero}. {descripcion}")
    try:
        resultado = operacion()
    except ErrorSistema as e:
        fallidas += 1
        print(f"   ERROR: {e}")
        if e.__cause__:
            print(f"   Causa: {e.__cause__}")
        logger.error(f"Operacion {numero} ({descripcion}): {e} | causa: {e.__cause__}")
    except Exception as e:
        # por si pasa algo que no se tenia previsto
        fallidas += 1
        print(f"   ERROR INESPERADO: {e}")
        logger.exception(f"Error inesperado en la operacion {numero}")
    else:
        exitosas += 1
        print(f"   OK -> {resultado}")
    finally:
        logger.info(f"Termino la operacion {numero}")


def desactivar_y_reservar():
    asesoria = sistema.buscar_servicio("Asesoria en redes")
    asesoria.disponible = False
    try:
        return sistema.hacer_reserva("80123456", "Asesoria en redes", 2)
    finally:
        asesoria.disponible = True


print("===== SISTEMA DE RESERVAS SOFTWARE FJ =====")
logger.info("Inicio de la simulacion")

# Clientes
ejecutar(1, "Registrar cliente valido", lambda: sistema.agregar_cliente(
    {"nombre": "Ana Gomez", "documento": "1012345678",
     "correo": "ana@gmail.com", "telefono": "3001234567"}))
ejecutar(2, "Registrar otro cliente valido", lambda: sistema.agregar_cliente(
    {"nombre": "Carlos Ruiz", "documento": "80123456",
     "correo": "carlos@hotmail.com", "telefono": "3115556677"}))
ejecutar(3, "Registrar cliente con correo malo", lambda: sistema.agregar_cliente(
    {"nombre": "Laura Perez", "documento": "52987654",
     "correo": "laura.gmail.com", "telefono": "3109876543"}))
ejecutar(4, "Registrar cliente con documento repetido", lambda: sistema.agregar_cliente(
    {"nombre": "Pedro Diaz", "documento": "1012345678",
     "correo": "pedro@gmail.com", "telefono": "3201112233"}))
ejecutar(5, "Registrar cliente sin telefono", lambda: sistema.agregar_cliente(
    {"nombre": "Sofia Rojas", "documento": "1098765432", "correo": "sofia@gmail.com"}))

# Servicios
ejecutar(6, "Crear sala de reuniones", lambda: sistema.agregar_servicio(
    ReservaSala("Sala principal", 50000, 10)))
ejecutar(7, "Crear alquiler de portatiles", lambda: sistema.agregar_servicio(
    AlquilerEquipo("Portatil", 40000, 1)))
ejecutar(8, "Crear asesoria", lambda: sistema.agregar_servicio(
    Asesoria("Asesoria en redes", 80000, "experto")))
ejecutar(9, "Crear servicio con precio negativo", lambda: sistema.agregar_servicio(
    ReservaSala("Sala pequena", -20000, 4)))
ejecutar(10, "Crear asesoria con nivel que no existe", lambda: sistema.agregar_servicio(
    Asesoria("Asesoria web", 60000, "maestro")))

# Reservas
ejecutar(11, "Reservar sala 3 horas", lambda: sistema.hacer_reserva(
    "1012345678", "Sala principal", 3))
ejecutar(12, "Reservar sala 12 horas (supera el maximo)", lambda: sistema.hacer_reserva(
    "80123456", "Sala principal", 12))
ejecutar(13, "Alquilar portatil 2 dias con 10% de descuento", lambda: sistema.hacer_reserva(
    "80123456", "Portatil", 2, 0.10))
ejecutar(14, "Alquilar portatil cuando ya no quedan", lambda: sistema.hacer_reserva(
    "1012345678", "Portatil", 1))
ejecutar(15, "Reserva de un cliente que no existe", lambda: sistema.hacer_reserva(
    "99999999", "Sala principal", 2))
ejecutar(16, "Reserva con descuento del 70%", lambda: sistema.hacer_reserva(
    "1012345678", "Asesoria en redes", 2, 0.70))
ejecutar(17, "Reservar asesoria desactivada", desactivar_y_reservar)
ejecutar(18, "Cancelar una reserva ya procesada", lambda: sistema.reservas[0].cancelar())
ejecutar(19, "Calcular costo de la sala de 3 formas", lambda: (
    sistema.servicios[0].calcular_costo(2),
    sistema.servicios[0].calcular_costo(2, 0.19),
    sistema.servicios[0].calcular_costo(2, 0.19, 0.10)))
ejecutar(20, "Reservar asesoria 2 horas", lambda: sistema.hacer_reserva(
    "80123456", "Asesoria en redes", 2))

print("\n===== RESUMEN =====")
print(f"Operaciones exitosas: {exitosas}")
print(f"Operaciones con error: {fallidas}")
print("Reservas:")
for r in sistema.reservas:
    print(" ", r)
print("Los errores quedaron guardados en logs/sistema.log")
logger.info("Fin de la simulacion")
