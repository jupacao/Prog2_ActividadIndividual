# Actividad Individual - Conultorio Odontológico
# Desarrollado por: Juan Pablo Castro Ocampo
# Universidad de Manizales
# Programación 2

class Client:
    def __init__(self, cedula, nombre, telefono, tipo_cliente):
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.tipo_cliente = tipo_cliente