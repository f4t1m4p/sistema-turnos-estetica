from functools import reduce

# MAGALI FUNCIONES DE TURNOS

def cargar_turnos():
    """
    Devuelve una lista con los turnos iniciales disponibles,
    incluyendo fecha, hora, profesional y servicio.
    """
    return [
        {"fecha_hora": ("2025-04-26", "10:00"), "profesional": "Gisela", "servicio": "Kapping"},
        {"fecha_hora": ("2025-04-25", "14:00"), "profesional": "Marisol", "servicio": "Semi"},
        {"fecha_hora": ("2025-04-26", "16:00"), "profesional": "Valentina", "servicio": "Soft Gel"},
    ]

def filtrar_turnos(turnos, servicio=None, profesional=None):
    """
    Filtra la lista de turnos por servicio y/o profesional.

    Parámetros:
        turnos (list): Lista de turnos disponibles.
        servicio (str or None): Nombre del servicio a filtrar (opcional).
        profesional (str or None): Nombre del profesional a filtrar (opcional).

    Retorna:
        list: Lista filtrada de turnos según los criterios dados.
    """
    return list(filter(lambda t:
        (servicio is None or t['servicio'] == servicio) and
        (profesional is None or t['profesional'] == profesional),
        turnos
    ))

def mostrar_turnos(turnos):
    """
    Imprime en pantalla la lista de turnos disponibles, mostrando fecha, hora, servicio y profesional.

    Parámetros:
        turnos (list): Lista de turnos disponibles.

    Retorna:
        None.
    """
    print("\nTurnos disponibles:")
    for i, turno in enumerate(turnos):
        fecha, hora = turno["fecha_hora"]
        print(f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}")


# FATIMA FUNCIONES DE RESERVA Y CANCELACION

def validar_documento(documento):
    """
    Valida que el documento contenga solo dígitos.

    Parámetros:
        documento (str): Documento ingresado por el usuario.

    Excepciones:
        ValueError: Si el documento no es numérico.
    """
    if not documento.isdigit():
        raise ValueError("El documento debe contener solo números.")

def reservar_turnos(turnos, reservas):
    """
    Permite al usuario seleccionar y reservar un turno de la lista disponible.
    Maneja excepciones y validaciones según los temas vistos en clase.

    Parámetros:
        turnos (list): Lista de turnos disponibles.
        reservas (list): Lista de reservas realizadas.

    Retorna:
        tuple: Listas actualizadas de turnos y reservas.
    """
    mostrar_turnos(turnos)
    nombres_existentes = {r["nombre"] for r in reservas}

    try:
        opcion = int(input("\nElija el número del turno que desea reservar: ")) - 1
        turno = turnos[opcion]
    except (ValueError, IndexError) as e:
        print(f"Error al seleccionar turno: {e}")
        return turnos, reservas

    try:
        nombre = input("Ingrese su nombre: ")
        if nombre in nombres_existentes:
            raise ValueError("Ya existe una reserva con ese nombre.")

        telefono = input("Ingrese su teléfono: ")
        documento = input("Ingrese su documento: ")
        validar_documento(documento)

        cliente = {
            "nombre": nombre,
            "telefono": telefono,
            "documento": documento,
            "turno": turno,
        }
        reservas.append(cliente)
        turnos = [t for t in turnos if t != turno]
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print(f"\nTurno reservado con éxito para {nombre}!")
    finally:
        print("Fin del intento de reserva.")

    return turnos, reservas

def cancelar_turno(turnos, reservas):
    """
    Cancela una reserva de turno según el documento ingresado por el usuario.

    Parámetros:
        turnos (list): Lista de turnos disponibles.
        reservas (list): Lista actual de reservas realizadas.

    Retorna:
        tuple: Listas actualizadas de turnos y reservas.
    """
    documento = input("Ingrese su documento para cancelar el turno: ")
    nuevas_reservas = []
    turno_recuperado = None

    for r in reservas:
        if r["documento"].lower() == documento.lower():
            turno_recuperado = r["turno"]
            print("Turno cancelado correctamente.")
        else:
            nuevas_reservas.append(r)

    if turno_recuperado:
        turnos.append(turno_recuperado)
    else:
        print("No se encontró una reserva con ese documento.")

    return turnos, nuevas_reservas


# GUI FUNCIONES DE CONSULTA Y ANALISIS

def ver_resumen_reservas(reservas):
    """
    Muestra un resumen agrupado de las reservas por profesional.

    Parámetros:
        reservas (list): Lista de diccionarios con información de las reservas.

    Retorna:
        None.
    """
    resumen = {}
    for r in reservas:
        profesional = r["turno"]["profesional"]
        resumen.setdefault(profesional, []).append(r)

    print("\n--- Resumen de Reservas ---")
    for profesional, lista in resumen.items():
        print(f"\nTurnos de {profesional}:")
        for r in lista:
            fecha, hora = r["turno"]["fecha_hora"]
            print(f"- {r['nombre']} el {fecha} a las {hora} para {r['turno']['servicio']}")
    print(f"\nTotal de reservas: {len(reservas)}")

def ver_nombre_clientes(reservas):
    """
    Muestra una lista única de nombres de clientes con turnos reservados.

    Parámetros:
        reservas (list): Lista de reservas realizadas.

    Retorna:
        None.
    """
    nombres = {r["nombre"] for r in reservas}
    print("Clientes con turnos reservados:")
    for nombre in nombres:
        print(f"- {nombre}")

def ver_servicios_y_profesionales(turnos):
    """
    Muestra los servicios y profesionales disponibles usando conjuntos.

    Parámetros:
        turnos (list): Lista de turnos disponibles.

    Retorna:
        None.
    """
    servicios = set(t["servicio"] for t in turnos)
    profesionales = set(t["profesional"] for t in turnos)
    print("\nServicios disponibles:", ', '.join(servicios))
    print("Profesionales disponibles:", ', '.join(profesionales))


# GUI MENU INTERACTIVO

def menu(turnos, reservas):
    """
    Muestra el menú principal del sistema y gestiona la interacción con el usuario.

    Parámetros:
        turnos (list): Lista de turnos disponibles.
        reservas (list): Lista de reservas realizadas.

    Retorna:
        None.
    """
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Ver turnos disponibles")
        print("2. Filtrar turnos")
        print("3. Reservar turno")
        print("4. Cancelar turno")
        print("5. Ver resumen de reservas")
        print("6. Ver nombres de clientes")
        print("7. Ver servicios y profesionales")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_turnos(turnos)
        elif opcion == "2":
            servicio = input("Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ").strip() or None
            profesional = input("Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ").strip() or None
            filtrados = filtrar_turnos(turnos, servicio, profesional)
            mostrar_turnos(filtrados)
        elif opcion == "3":
            turnos, reservas = reservar_turnos(turnos, reservas)
        elif opcion == "4":
            turnos, reservas = cancelar_turno(turnos, reservas)
        elif opcion == "5":
            ver_resumen_reservas(reservas)
        elif opcion == "6":
            ver_nombre_clientes(reservas)
        elif opcion == "7":
            ver_servicios_y_profesionales(turnos)
        elif opcion == "0":
            print("Gracias por usar el sistema de turnos. ¡Hasta luego!")
            break
        else:
            print("Opción inválida")


# GUI EJECUCIÓN

def main():
    """
    Función principal que inicializa el sistema de turnos y llama al menú principal.

    Retorna:
        None.
    """
    turnos = cargar_turnos()
    reservas = []
    menu(turnos, reservas)

if __name__ == "__main__":
    main()