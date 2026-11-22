# Software FJ - Sistema de reservas

Proyecto de la Fase 4 del curso Programación (213023) de la UNAD.

Sistema en Python para manejar clientes, servicios y reservas de la empresa Software FJ, que ofrece salas, alquiler de equipos y asesorías. No usa base de datos: todo se guarda en listas y los errores y eventos se escriben en `logs/sistema.log`.

## Cómo ejecutarlo

Se necesita Python 3.10 o superior. No hay que instalar librerías.

```
python main.py
```

## Archivos

- `excepciones.py`: excepciones personalizadas (todas heredan de `ErrorSistema`).
- `logger.py`: configuración del archivo de log.
- `entidad.py`: clase abstracta `Entidad`.
- `cliente.py`: clase `Cliente` con atributos privados y validaciones.
- `servicios.py`: clase abstracta `Servicio` y las clases `ReservaSala`, `AlquilerEquipo` y `Asesoria`.
- `reserva.py`: clase `Reserva` con los métodos confirmar, cancelar y procesar.
- `sistema.py`: clase `SistemaReservas`, que guarda las listas y hace las operaciones.
- `main.py`: simulación de 20 operaciones (válidas y con errores).

## Manejo de excepciones

- `try/except`: en `sistema.py` al registrar clientes y buscar datos.
- `try/except/else`: en `Reserva.confirmar()`.
- `try/finally`: en `Reserva.cancelar()`.
- `try/except/else/finally`: en `Reserva.procesar()` y en la función `ejecutar()` de `main.py`.
- Encadenamiento (`raise ... from e`): por ejemplo, cuando falta un dato del cliente, el `TypeError` se convierte en `ParametroFaltanteError`.

## Autor

- Juan Felipe Valencia Sanchez - 1067590003
