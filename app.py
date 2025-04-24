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