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

from turnos import cargar_turnos, mostrar_turnos, filtrar_turnos
from reservas import reservar_turno, cancelar_turno

def ver_resumen_reservas(reservas):
    """Muestra un resumen de todas las reservas."""
    print("\n--- Resumen de Reservas ---")
    for r in reservas:
        t = r["turno"]
        print(f"{r['nombre']}: {t['fecha']} {t['hora']} - {t['servicio']} con {t['profesional']}")
    print(f"\nTotal de reservas: {len(reservas)}")

def ver_clientes(reservas):
    """Lista los nombres de los clientes con reservas."""
    print("\n--- Clientes con reservas ---")
    for r in reservas:
        print(f"- {r['nombre']}")

def menu_principal():
    """Menú interactivo del sistema."""
    turnos = cargar_turnos()
    reservas = []

