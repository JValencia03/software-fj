import re

from entidad import Entidad
from excepciones import ClienteInvalidoError


class Cliente(Entidad):

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # se asignan con los setters para que se validen
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre invalido: {valor}")
        if not valor.replace(" ", "").isalpha():
            raise ClienteInvalidoError(f"El nombre solo puede tener letras: {valor}")
        self.__nombre = valor.strip().title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        valor = str(valor)
        if not valor.isdigit() or not (6 <= len(valor) <= 10):
            raise ClienteInvalidoError(f"Documento invalido: {valor}")
        self.__documento = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not re.match(r"^[\w.-]+@[\w-]+\.[\w.]+$", str(valor)):
            raise ClienteInvalidoError(f"Correo invalido: {valor}")
        self.__correo = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        valor = str(valor)
        if not valor.isdigit() or not (7 <= len(valor) <= 10):
            raise ClienteInvalidoError(f"Telefono invalido: {valor}")
        self.__telefono = valor

    def mostrar_info(self):
        return f"Cliente {self.id}: {self.nombre} - doc {self.documento} - {self.correo}"
