"""
Módulo de persistencia de datos para el sistema de turnos.
Maneja la carga y guardado de datos en archivos JSON.
"""

import json
import os
from datetime import datetime

def cargar_turnos():
    """
    Carga los turnos disponibles desde el archivo JSON.
    FUNCIONALIDAD: Cargar información de turnos disponibles
    """
    try:
        with open("turnos.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def guardar_turnos(turnos):
    """
    Guarda los turnos disponibles en el archivo JSON.
    FUNCIONALIDAD: Guardar cambios en los turnos disponibles
    """
    with open("turnos.json", "w", encoding="utf-8") as archivo:
        json.dump(turnos, archivo, indent=4, ensure_ascii=False)

def cargar_reservas():
    """
    Carga las reservas desde el archivo JSON.
    FUNCIONALIDAD: Cargar información de reservas existentes
    """
    try:
        with open("reservas.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def guardar_reservas(reservas):
    """
    Guarda las reservas en el archivo JSON.
    FUNCIONALIDAD: Guardar cambios en las reservas
    """
    with open("reservas.json", "w", encoding="utf-8") as archivo:
        json.dump(reservas, archivo, indent=4, ensure_ascii=False)

def crear_backup():
    """
    Crea un backup de los archivos de datos.
    FUNCIONALIDAD: Proteger datos importantes
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Backup de turnos
    if os.path.exists("turnos.json"):
        backup_turnos = f"turnos_backup_{timestamp}.json"
        with open("turnos.json", "r", encoding="utf-8") as original:
            with open(backup_turnos, "w", encoding="utf-8") as backup:
                backup.write(original.read())
    
    # Backup de reservas
    if os.path.exists("reservas.json"):
        backup_reservas = f"reservas_backup_{timestamp}.json"
        with open("reservas.json", "r", encoding="utf-8") as original:
            with open(backup_reservas, "w", encoding="utf-8") as backup:
                backup.write(original.read())
    
    return timestamp

def restaurar_backup(timestamp):
    """
    Restaura los archivos desde un backup específico.
    FUNCIONALIDAD: Recuperar datos en caso de problemas
    """
    backup_turnos = f"turnos_backup_{timestamp}.json"
    backup_reservas = f"reservas_backup_{timestamp}.json"
    
    if os.path.exists(backup_turnos):
        with open(backup_turnos, "r", encoding="utf-8") as backup:
            with open("turnos.json", "w", encoding="utf-8") as original:
                original.write(backup.read())
    
    if os.path.exists(backup_reservas):
        with open(backup_reservas, "r", encoding="utf-8") as backup:
            with open("reservas.json", "w", encoding="utf-8") as original:
                original.write(backup.read()) 