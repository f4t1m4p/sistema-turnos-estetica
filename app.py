from functools import reduce

def filtrar_turnos(turnos, servicio=None, profesional=None):
    """Filtra la lista de turnos por servicio y/o profesional."""
    filtrados = list(filter(lambda t:
        (servicio is None or t['servicio'] == servicio) and
        (profesional is None or t['profesional'] == profesional),
        turnos
    ))
    return filtrados

def cargar_turnos():
    """Devuelve una lista con los turnos iniciales disponibles."""
    return [
        {"fecha": "2025-04-26", "hora": "10:00", "profesional": "Gisela", "servicio": "Kapping"},
        {"fecha": "2025-04-25", "hora": "14:00", "profesional": "Marisol", "servicio": "Semi"},
        {"fecha": "2025-04-26", "hora": "16:00", "profesional": "Valentina", "servicio": "Soft Gel"},
    ]

def mostrar_turnos(turnos):
    """Muestra en pantalla los turnos disponibles."""
    print("\nTurnos disponibles:")
    for i, turno in enumerate(turnos):
        print(f"{i + 1}. {turno['fecha']}{turno['hora']} - {turno['servicio']} con {turno['profesional']}")
        
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