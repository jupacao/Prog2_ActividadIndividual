# Actividad Individual - Conultorio Odontológico
# Desarrollado por: Juan Pablo Castro Ocampo
# Universidad de Manizales
# Programación 2

from models.client import Client
from models.appointment import Appointment
from datetime import datetime

def es_invalido_por_patron(cadena):
    # 1. Verifica si todos los números son exactamente iguales (ej. 1111111)
    if len(set(cadena)) == 1:
        return True
    
    # 2. Verifica si son consecutivos ascendentes (ej. 1234567) o descendentes (ej. 7654321)
    es_ascendente = all(int(cadena[i]) == int(cadena[i-1]) + 1 for i in range(1, len(cadena)))
    es_descendente = all(int(cadena[i]) == int(cadena[i-1]) - 1 for i in range(1, len(cadena)))
    
    return es_ascendente or es_descendente

def capturar_datos():
    print("\n--- INGRESO DE DATOS DEL CLIENTE ---")
    
    # Validación Cédula
    while True:
        cedula = input("Cédula: ")
        if not (cedula.isdigit() and 7 <= len(cedula) <= 10):
            print("Error: La cédula debe ser un número entre 7 y 10 dígitos.")
        elif es_invalido_por_patron(cedula):
            print("Error: La cédula no puede estar formada por números todos iguales ni consecutivos.")
        else:
            break

    # Validación Nombre
    while True:
        nombre = input("Nombre: ")
        if nombre.replace(" ", "").isalpha():
            break
        print("Error: El nombre debe contener únicamente letras.")

    # Validación Apellido
    while True:
        apellido = input("Apellido: ")
        if apellido.replace(" ", "").isalpha():
            break
        print("Error: El apellido debe contener únicamente letras.")

    # Validación Teléfono
    while True:
        telefono = input("Teléfono: ")
        if not (telefono.isdigit() and len(telefono) == 10):
            print("Error: El teléfono debe ser un número de 10 dígitos.")
        elif not telefono.startswith(('3', '6')):
            print("Error: El teléfono debe iniciar obligatoriamente con el número 3 o 6.")
        elif es_invalido_por_patron(telefono):
            print("Error: El teléfono no puede estar formado por números todos iguales ni consecutivos.")
        else:
            break
    
    # Menú Tipo de Cliente
    print("Tipo de Cliente (1. Particular, 2. EPS, 3. Prepagada)")
    tipos_c = {"1": "Particular", "2": "EPS", "3": "Prepagada"}
    while True:
        opcion_c = input("Seleccione opción (1 - 2 - 3): ")
        if opcion_c in tipos_c:
            tipo_cliente = tipos_c[opcion_c]
            break
        print("Error: Seleccione una opción válida (1, 2 o 3).")
    
    # Menú Tipo de Atención
    print("Tipo de Atención (1. Limpieza, 2. Calzas, 3. Extracción, 4. Diagnóstico)")
    tipos_a = {"1": "Limpieza", "2": "Calzas", "3": "Extracción", "4": "Diagnóstico"}
    while True:
        opcion_a = input("Seleccione opción (1 - 2 - 3 - 4): ")
        if opcion_a in tipos_a:
            tipo_atencion = tipos_a[opcion_a]
            break
        print("Error: Seleccione una opción válida (1, 2, 3 o 4).")
    
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
                
    # Menú Prioridad
    print("Prioridad de Atención (1. Normal, 2. Urgente)")
    tipos_p = {"1": "Normal", "2": "Urgente"}
    while True:
        opcion_p = input("Seleccione opción (1 - 2): ")
        if opcion_p in tipos_p:
            prioridad = tipos_p[opcion_p]
            break
        print("Error: Seleccione una opción válida (1 o 2).")

    # Validación Fecha
    fecha_actual = datetime.now().date()
    while True:
        fecha_cita = input("Fecha de la cita (DD/MM/AAAA): ")
        try:
            fecha_obj = datetime.strptime(fecha_cita, "%d/%m/%Y").date()
            if fecha_obj < fecha_actual:
                print("Error: La fecha de la cita no puede ser anterior al día de hoy.")
            elif fecha_obj.weekday() == 6:
                print("Error: El consultorio no atiende los domingos. Por favor seleccione otro día.")
            else:
                break
        except ValueError:
            print("Error: Ingrese una fecha válida usando el formato DD/MM/AAAA.")

    nuevo_cliente = Client(cedula, nombre, apellido, telefono, tipo_cliente)
    nueva_cita = Appointment(nuevo_cliente, tipo_atencion, cantidad, prioridad, fecha_cita)
    
    return nueva_cita

def main():
    lista_citas = []
    continuar = "s"
    
    while continuar.lower() == "s":
        cita = capturar_datos()
        lista_citas.append(cita)
        while True:
            continuar = input("\n¿Desea ingresar otro cliente? (S/N): ").lower()
            if continuar in ["s", "n"]:
                break
            print("Error: Escriba 'S' para sí o 'N' para no.")

    total_clientes = len(lista_citas)
    ingresos_totales = sum(cita.valor_total for cita in lista_citas)
    extracciones = sum(1 for cita in lista_citas if cita.tipo_atencion == "Extracción")

    print("\n" + "="*40)
    print("--- RESULTADOS DEL CONSULTORIO ---")
    print(f"1. Total clientes: {total_clientes}")
    print(f"2. Ingresos totales recibidos: ${ingresos_totales:,}")
    print(f"3. Número de clientes para extracción: {extracciones}")
    print("="*40)

    citas_ordenadas = sorted(lista_citas, key=lambda x: x.valor_atencion, reverse=True)
    
    print("\n--- LISTA ORDENADA POR VALOR DE ATENCIÓN (Mayor a menor) ---")
    for cita in citas_ordenadas:
        print(f"Paciente: {cita.client.nombre} {cita.client.apellido} - Cédula: {cita.client.cedula} - Atención: {cita.tipo_atencion} - Valor: ${cita.valor_atencion:,}")

    print("\n--- BÚSQUEDA DE CLIENTE ---")
    cedula_buscar = input("Ingrese la cédula del cliente a buscar: ")
    
    encontrado = False
    for cita in citas_ordenadas:
        if cita.client.cedula == cedula_buscar:
            print("\n¡Cliente encontrado!")
            print(f"Paciente: {cita.client.nombre} {cita.client.apellido}")
            print(f"Teléfono: {cita.client.telefono}")
            print(f"Prioridad: {cita.prioridad}")
            print(f"Fecha cita: {cita.fecha_cita}")
            print(f"Tipo Atención: {cita.tipo_atencion} ({cita.cantidad})")
            print(f"Valor a pagar: ${cita.valor_total:,}")
            encontrado = True
            break
            
    if not encontrado:
        print("Cliente no encontrado en el sistema.")

if __name__ == "__main__":
    main()