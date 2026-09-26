# Actividad Individual - Conultorio Odontológico
# Desarrollado por: Juan Pablo Castro Ocampo
# Universidad de Manizales
# Programación 2

from models.client import Client
from models.appointment import Appointment

def capturar_datos():
    print("\n--- INGRESO DE DATOS DEL CLIENTE ---")
    cedula = input("Cédula: ")
    nombre = input("Nombre: ")
    telefono = input("Teléfono: ")
    
    print("Tipo de Cliente (1. Particular, 2. EPS, 3. Prepagada)")
    tipos_c = {"1": "Particular", "2": "EPS", "3": "Prepagada"}
    tipo_cliente = tipos_c.get(input("Seleccione opción (1/2/3): "), "Particular")
    
    print("Tipo de Atención (1. Limpieza, 2. Calzas, 3. Extracción, 4. Diagnóstico)")
    tipos_a = {"1": "Limpieza", "2": "Calzas", "3": "Extracción", "4": "Diagnóstico"}
    tipo_atencion = tipos_a.get(input("Seleccione opción (1/2/3/4): "), "Diagnóstico")
    
    if tipo_atencion in ["Limpieza", "Diagnóstico"]:
        cantidad = 1
        print(f"Cantidad asignada automáticamente: 1 (por ser {tipo_atencion})")
    else:
        while True:
            try:
                cantidad = int(input(f"Cantidad de {tipo_atencion} (mayor a 0): "))
                if cantidad > 0:
                    break
                print("Error: La cantidad debe ser mayor a cero.")
            except ValueError:
                print("Por favor, ingrese un número válido.")
                
    prioridad = input("Prioridad (Normal/Urgente): ").capitalize()
    fecha_cita = input("Fecha de la cita (DD/MM/AAAA): ")

    nuevo_cliente = Client(cedula, nombre, telefono, tipo_cliente)
    nueva_cita = Appointment(nuevo_cliente, tipo_atencion, cantidad, prioridad, fecha_cita)
    
    return nueva_cita

def main():
    lista_citas = []
    continuar = "s"
    
    while continuar.lower() == "s":
        cita = capturar_datos()
        lista_citas.append(cita)
        continuar = input("\n¿Desea ingresar otro cliente? (s/n): ")

    total_clientes = len(lista_citas)
    ingresos_totales = sum(cita.valor_total for cita in lista_citas)
    extracciones = sum(1 for cita in lista_citas if cita.tipo_atencion == "Extracción")

    print("\n" + "="*40)
    print("--- RESULTADOS DEL CONSULTORIO ---")
    print(f"1. Total Clientes: {total_clientes}")
    print(f"2. Ingresos Totales Recibidos: ${ingresos_totales:,}")
    print(f"3. Número de clientes para Extracción: {extracciones}")
    print("="*40)

    citas_ordenadas = sorted(lista_citas, key=lambda x: x.valor_atencion, reverse=True)
    
    print("\n--- LISTA ORDENADA POR VALOR DE ATENCIÓN (Mayor a Menor) ---")
    for cita in citas_ordenadas:
        print(f"Nombre: {cita.client.nombre} - Cédula: {cita.client.cedula} - Atención: {cita.tipo_atencion} - Valor Atención: ${cita.valor_atencion:,}")

    print("\n--- BÚSQUEDA DE CLIENTE ---")
    cedula_buscar = input("Ingrese la cédula a buscar en la lista ordenada: ")
    
    encontrado = False
    for cita in citas_ordenadas:
        if cita.client.cedula == cedula_buscar:
            print("\n¡Cliente encontrado!")
            print(f"Nombre: {cita.client.nombre}")
            print(f"Teléfono: {cita.client.telefono}")
            print(f"Tipo Atención: {cita.tipo_atencion} ({cita.cantidad})")
            print(f"Valor a pagar: ${cita.valor_total:,}")
            encontrado = True
            break
            
    if not encontrado:
        print("Cliente no encontrado en el sistema.")

if __name__ == "__main__":
    main()