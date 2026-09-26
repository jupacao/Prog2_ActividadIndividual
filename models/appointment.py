# Actividad Individual - Conultorio Odontológico
# Desarrollado por: Juan Pablo Castro Ocampo
# Universidad de Manizales
# Programación 2

class Appointment:
    def __init__(self, client, tipo_atencion, cantidad, prioridad, fecha_cita):
        self.client = client  # Objeto de tipo Client
        self.tipo_atencion = tipo_atencion
        self.cantidad = cantidad
        self.prioridad = prioridad
        self.fecha_cita = fecha_cita
        
        self.valor_cita = 0
        self.valor_atencion = 0
        self.valor_total = 0
        
        self.calcular_totales()

    def calcular_totales(self):
        tarifas_cita = {"Particular": 80000, "EPS": 5000, "Prepagada": 30000}
        tarifas_atencion = {
            "Particular": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000},
            "EPS": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0},
            "Prepagada": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}
        }

        tipo_c = self.client.tipo_cliente
        
        self.valor_cita = tarifas_cita.get(tipo_c, 0)
        valor_unitario = tarifas_atencion.get(tipo_c, {}).get(self.tipo_atencion, 0)
        
        self.valor_atencion = valor_unitario * self.cantidad
        self.valor_total = self.valor_cita + self.valor_atencion