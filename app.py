from functools import reduce

#FATIMA FUNCIONES DE TURNOS
def cargar_turnos():
    """Devuelve una lista con los turnos iniciales disponibles, incluyendo fecha, hora, profesional y servicio."""
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

#from turnos import cargar_turnos, mostrar_turnos, filtrar_turnos
#from reservas import reservar_turno, cancelar_turno

def reservar_turnos(turnos, reservas):
    """
    Permite al usuario seleccionar y reservar un turno de la lista disponible.
    Muestra los turnos disponibles, solicita al usuario que elija uno y luego pide su nombre y teléfono.
    Verifica que no haya una reserva previa con el mismo nombre para evitar duplicados.

    Parámetros:
        turnos (list): Lista de turnos disponibles.
        reservas (list): Lista actual de reservas realizadas.

    Retorna:
        tuple: Una tupla con la lista actualizada de turnos y reservas.
    """
    mostrar_turnos(turnos)
    nombres_existentes = {r["nombre"] for r in reservas}

    try:
        opcion = int(input("\nElija el número del turno que desea reservar:")) - 1
        turno = turnos[opcion]
    except (ValueError, IndexError):
        print("Opción inválida")
        return turnos, reservas

    nombre = input("Ingrese su nombre: ")
    if nombre in nombres_existentes:
        print("Ya existe una reserva con ese nombre.")
        return turnos, reservas

    telefono = input("Ingrese su teléfono: ")

    cliente = {
        "nombre": nombre,
        "telefono": telefono,
        "turno": turno,
    }

    reservas.append(cliente)
    turnos = [t for t in turnos if t != turno]
    print(f"\nTurno reservado con éxito para {nombre}!")
    return turnos, reservas

def cancelar_turno(turnos, reservas):
    """
    Cancela una reserva de turno según el nombre ingresado por el usuario.
    Elimina la reserva y vuelve a agregar el turno a la lista de turnos disponibles.

    Parámetros:
        turnos (list): Lista de turnos disponibles.
        reservas (list): Lista actual de reservas realizadas.

    Retorna:
        tuple: Una tupla con la lista actualizada de turnos y reservas.
    """
    nombre = input("Ingrese su nombre para cancelar el turno: ")
    nuevas_reservas = []
    turno_recuperado = None

    for r in reservas:
        if r["nombre"].lower() == nombre.lower():
            turno_recuperado = r["turno"]
            print("Turno cancelado correctamente.")
        else:
            nuevas_reservas.append(r)

    if turno_recuperado:
        turnos.append(turno_recuperado)
    else:
        print("No se encontró una reserva con ese nombre.")

    return turnos, nuevas_reservas
