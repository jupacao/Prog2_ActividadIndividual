# Actividad Individual - Conultorio Odontológico
# Desarrollado por: Juan Pablo Castro Ocampo
# Universidad de Manizales
# Programación 2

from models.client import Client
from models.appointment import Appointment
from datetime import datetime
import holidays

def es_invalido_por_patron(cadena):
    if len(set(cadena)) == 1:
        return True
    es_ascendente = all(int(cadena[i]) == int(cadena[i-1]) + 1 for i in range(1, len(cadena)))
    es_descendente = all(int(cadena[i]) == int(cadena[i-1]) - 1 for i in range(1, len(cadena)))
    return es_ascendente or es_descendente

def capturar_datos():
    print("\n--- INGRESO DE DATOS DEL CLIENTE ---")
    while True:
        cedula = input("Cédula: ")
        if not (cedula.isdigit() and 7 <= len(cedula) <= 10):
            print("Error: Verifique la cédula.")
        elif es_invalido_por_patron(cedula):
            print("Error: Verifique la cédula.")
        else:
            break
    
    while True:
        nombre = input("Nombre: ")
        if nombre.replace(" ", "").isalpha():
            break
        print("Error: El nombre no puede contener números.")
    
    while True:
        apellido = input("Apellido: ")
        if apellido.replace(" ", "").isalpha():
            break
        print("Error: El apellido no puede contener números.")
    
    while True:
        telefono = input("Teléfono: ")
        if not (telefono.isdigit() and len(telefono) == 10):
            print("Error: Verifique el teléfono, debe ser de 10 dígitos.")
        elif not telefono.startswith(('3', '6')):
            print("Error: Verifique el teléfono, debe iniciar con 3 (Celular) o 6 (Fijo).")
        elif es_invalido_por_patron(telefono):
            print("Error: Verifique el teléfono.")
        else:
            break

    print("Tipo de cliente (1 - Particular, 2 - EPS, 3 - Prepagada)")
    tipos_c = {"1": "Particular", "2": "EPS", "3": "Prepagada"}
    while True:
        opcion_c = input("Seleccione la opción: ")
        if opcion_c in tipos_c:
            tipo_cliente = tipos_c[opcion_c]
            break
        print("Error: Seleccione una opción válida (1 - Particular, 2 - EPS, 3 - Prepagada).")
    
    print("Tipo de Atención (1 - Limpieza, 2 - Calzas, 3 - Extracción, 4 - Diagnóstico)")
    tipos_a = {"1": "Limpieza", "2": "Calzas", "3": "Extracción", "4": "Diagnóstico"}
    while True:
        opcion_a = input("Seleccione la opción: ")
        if opcion_a in tipos_a:
            tipo_atencion = tipos_a[opcion_a]
            break
        print("Error: Seleccione una opción válida (1 - Limpieza, 2 - Calzas, 3 - Extracción, 4 - Diagnóstico).")
    
    # --- VALIDACIÓN DE CANTIDAD CON LÍMITES MÁXIMOS ---
    if tipo_atencion in ["Limpieza", "Diagnóstico"]:
        cantidad = 1
    else:
        while True:
            try:
                cantidad = int(input(f"Ingrese la cantidad: "))
                if cantidad <= 0:
                    print("Error: La cantidad debe ser mayor a cero.")
                elif tipo_atencion == "Calzas" and cantidad > 10:
                    print("Error: El límite máximo de calzas por sesión es de 10.")
                elif tipo_atencion == "Extracción" and cantidad > 8:
                    print("Error: El límite máximo de extracciones por sesión es de 8.")
                else:
                    break
            except ValueError:
                print("Error: Por favor, ingrese un número válido.")
                
    print("Prioridad de Atención (1 - Normal, 2 - Urgente)")
    tipos_p = {"1": "Normal", "2": "Urgente"}
    while True:
        opcion_p = input("Seleccione la opción: ")
        if opcion_p in tipos_p:
            prioridad = tipos_p[opcion_p]
            break
        print("Error: Seleccione una opción válida (1 - Normal, 2 - Urgente).")

    # Validación Fecha y Festivos
    fecha_actual = datetime.now().date()
    festivos_colombia = holidays.CO(language='es') 
    while True:
        fecha_cita = input("Fecha de la cita (DD/MM/AAAA): ")
        try:
            fecha_obj = datetime.strptime(fecha_cita, "%d/%m/%Y").date()
            if fecha_obj < fecha_actual:
                print("Error: La fecha de la cita no puede ser anterior al día de hoy.")
            elif fecha_obj.weekday() == 6:
                print("Error: El consultorio no atiende los domingos. Por favor seleccione otro día.")
            elif fecha_obj in festivos_colombia:
                nombre_festivo = festivos_colombia.get(fecha_obj)
                print(f"Error: El consultorio no atiende en días festivos ({nombre_festivo}). Por favor seleccione otro día.")
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
            print("Error: Escriba 'S' para Sí o 'N' para No.")
            
    total_clientes = len(lista_citas)
    ingresos_totales = sum(cita.valor_total for cita in lista_citas)
    extracciones = sum(1 for cita in lista_citas if cita.tipo_atencion == "Extracción")
    
    print("\n" + "="*40)
    print("--- RESULTADOS DEL CONSULTORIO ---")
    print(f"1. Total de clientes: {total_clientes}")
    print(f"2. Ingresos totales recibidos: ${ingresos_totales:,}")
    print(f"3. Número de clientes para extracción: {extracciones}")
    print("="*40)

    citas_ordenadas = sorted(lista_citas, key=lambda x: x.valor_atencion, reverse=True)
    
    print("\n--- LISTA ORDENADA POR VALOR DE ATENCIÓN (Mayor a menor) ---")
    for cita in citas_ordenadas:
        print(f"Paciente: {cita.client.nombre} {cita.client.apellido} - Cédula: {cita.client.cedula} - Atención: {cita.tipo_atencion} - Valor: ${cita.valor_atencion:,}")
        
    print("\n--- BÚSQUEDA DE CLIENTE ---")
    while True:
        cedula_buscar = input("\nIngrese la cédula del cliente: ")
        encontrado = False
        for cita in citas_ordenadas:
            if cita.client.cedula == cedula_buscar:
                print("\n¡Cliente encontrado!")
                print(f"Paciente: {cita.client.nombre} {cita.client.apellido}")
                print(f"Teléfono: {cita.client.telefono}")
                print(f"Tipo de cliente: {cita.client.tipo_cliente}") 
                print(f"Prioridad: {cita.prioridad}")
                print(f"Fecha de cita: {cita.fecha_cita}")
                print(f"Tipo de atención: {cita.tipo_atencion} ({cita.cantidad})")
                print(f"Valor a pagar: ${cita.valor_total:,}")
                encontrado = True
                break      
        if not encontrado:
            print("Cliente no encontrado en el sistema.")    
        while True:
            reintentar = input("\n¿Desea buscar otra cédula? (S/N): ").lower()
            if reintentar in ['s', 'n']:
                break
            print("Error: Escriba 'S' para Sí o 'N' para No.")    
        if reintentar == 'n':
            break

if __name__ == "__main__":
    main()