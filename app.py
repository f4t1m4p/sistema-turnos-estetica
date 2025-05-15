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
    mostrar_turnos(turnos)
    try:
        opcion= int(input("\nElija el número del turno que desea reservar:")) -1
        turno = turnos[opcion]
    except (ValueError, IndexError):
        print("opcion invalida")
        return turnos, reservas
    
    nombre = input("ingrese su nombre: ")
    telefono = input("ingrese su telefono: ")
    
    cliente = {
        "nombre": nombre,
        "telefono": telefono,
        "turno": turno,
    }    
    
    reservas.append(cliente)        
    turnos =  [t for t in turnos if t != turno]
    print(f"\nTurno reservado con éxito para {nombre}!")  
    return turnos, reservas

def cancelar_turno(turnos, reservas):
    
    nombre = input("ingrese su nombre para cancelar turnos: ")
    nuevas_reservas = []
    turno_recuperado = None    
    
    for r in reservas:
        if r["nombre"].lower() == nombre.lower():
            turno_recuperado = r["turno"]
            print("Turno cancelado correctamente")
        else:
            nuevas_reservas.append(r)
    
    if turno_recuperado:
        turnos.append(turno_recuperado)
    else:
        print("No se encontro una reserva con ese nombre.")
    return turnos,nuevas_reservas