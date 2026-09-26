# Actividad Individual - Conultorio Odontológico
# Desarrollado por: Juan Pablo Castro Ocampo
# Universidad de Manizales
# Programación 2

class Client:
    def __init__(self, cedula, nombre, apellido, telefono, tipo_cliente):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido  # Nuevo atributo
        self.telefono = telefono
        self.tipo_cliente = tipo_cliente