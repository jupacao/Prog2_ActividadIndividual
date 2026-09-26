# Actividad Individual - Conultorio Odontológico
# Desarrollado por: Juan Pablo Castro Ocampo
# Universidad de Manizales
# Programación 2

from models.client import Client
from models.appointment import Appointment
from datetime import datetime

def capturar_datos():
    print("\n--- INGRESO DE DATOS DEL CLIENTE ---")
    
    # Validación Cédula (Solo números)
    while True:
        cedula = input("Cédula: ")
        if cedula.isdigit():
            break
        print("Error: La cédula debe contener únicamente números.")

    # Validación Nombre (Solo letras y espacios)
    while True:
        nombre = input("Nombre: ")
        if nombre.replace(" ", "").isalpha():
            break
        print("Error: El nombre debe contener únicamente letras.")

    # Validación Teléfono (Solo números)
    while True:
        telefono = input("Teléfono: ")
        if telefono.isdigit():
            break
        print("Error: El teléfono debe contener únicamente números.")
    
    # Validación Menú Cliente
    print("Tipo de Cliente (1. Particular, 2. EPS, 3. Prepagada)")
    tipos_c = {"1": "Particular", "2": "EPS", "3": "Prepagada"}
    while True:
        opcion_c = input("Seleccione opción (1/2/3): ")
        if opcion_c in tipos_c:
            tipo_cliente = tipos_c[opcion_c]
            break
        print("Error: Seleccione una opción numérica válida (1, 2 o 3).")
    
    # Validación Menú Atención
    print("Tipo de Atención (1. Limpieza, 2. Calzas, 3. Extracción, 4. Diagnóstico)")
    tipos_a = {"1": "Limpieza", "2": "Calzas", "3": "Extracción", "4": "Diagnóstico"}
    while True:
        opcion_a = input("Seleccione opción (1/2/3/4): ")
        if opcion_a in tipos_a:
            tipo_atencion = tipos_a[opcion_a]
            break
        print("Error: Seleccione una opción numérica válida (1, 2, 3 o 4).")
    
    # Validación Cantidad
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
                print("Error: Por favor, ingrese un número válido.")
                
    # Validación Prioridad
    while True:
        prioridad = input("Prioridad (Normal/Urgente): ").capitalize()
        if prioridad in ["Normal", "Urgente"]:
            break
        print("Error: Escriba exactamente 'Normal' o 'Urgente'.")

    # Validación Fecha
    while True:
        fecha_cita = input("Fecha de la cita (DD/MM/AAAA): ")
        try:
            # Intenta convertir el texto a una fecha real para validar el formato
            datetime.strptime(fecha_cita, "%d/%m/%Y")
            break
        except ValueError:
            print("Error: Ingrese una fecha válida usando el formato DD/MM/AAAA (ej. 26/09/2026).")

    # Instanciamos los objetos con datos limpios y validados
    nuevo_cliente = Client(cedula, nombre, telefono, tipo_cliente)
    nueva_cita = Appointment(nuevo_cliente, tipo_atencion, cantidad, prioridad, fecha_cita)
    
    return nueva_cita

def main():
    lista_citas = []
    continuar = "s"
    
    while continuar.lower() == "s":
        cita = capturar_datos()
        lista_citas.append(cita)
        while True:
            continuar = input("\n¿Desea ingresar otro cliente? (s/n): ").lower()
            if continuar in ["s", "n"]:
                break
            print("Error: Escriba 's' para sí o 'n' para no.")

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