import json
import os
from datetime import datetime, timedelta
import logging
import random

logging.basicConfig(
    filename='sistema_turnos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ARCHIVO_TURNOS = "turnos.json"
ARCHIVO_RESERVAS = "reservas.json"

def generar_turnos_iniciales():
    """
    Genera una lista de turnos para los próximos 3 meses.
    """
    turnos = []
    servicios = ["Kapping", "Semi", "Soft Gel"]
    profesionales = ["Gisela", "Marisol", "Valentina"]
    horas = ["10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00"]
    

    fecha_actual = datetime.now()
    fecha_fin = fecha_actual + timedelta(days=90) 
    
    fecha = fecha_actual
    while fecha <= fecha_fin:

        if fecha.weekday() < 5:  
            for hora in horas:

                for _ in range(random.randint(2, 3)):
                    turno = {
                        "fecha_hora": [fecha.strftime("%Y-%m-%d"), hora],
                        "profesional": random.choice(profesionales),
                        "servicio": random.choice(servicios)
                    }
                    turnos.append(turno)
        fecha += timedelta(days=1)
    
    return turnos

def guardar_turnos(turnos):
    """
    Guarda los turnos en un archivo.
    """
    try:
        turnos_serializables = []
        for turno in turnos:
            turno_copia = turno.copy()
            if isinstance(turno_copia["fecha_hora"], tuple):
                turno_copia["fecha_hora"] = list(turno_copia["fecha_hora"])
            turnos_serializables.append(turno_copia)

        with open(ARCHIVO_TURNOS, 'w', encoding='utf-8') as archivo:
            json.dump(turnos_serializables, archivo, ensure_ascii=False, indent=4)
            
        logging.info(f"Turnos guardados exitosamente en {ARCHIVO_TURNOS}")
    except Exception as e:
        logging.error(f"Error al guardar turnos: {str(e)}")
        raise

def cargar_turnos():
    """
    Carga los turnos desde un archivo.
    """
    try:
        if not os.path.exists(ARCHIVO_TURNOS):
            turnos_iniciales = [

                {"fecha_hora": ["2025-01-27", "09:00"], "profesional": "Valentina", "servicio": "Soft Gel"},
                {"fecha_hora": ["2025-01-27", "12:00"], "profesional": "Valentina", "servicio": "Semi"},
                
                {"fecha_hora": ["2025-01-27", "09:00"], "profesional": "Marisol", "servicio": "Kapping"},
                {"fecha_hora": ["2025-01-27", "10:30"], "profesional": "Marisol", "servicio": "Semi"},
                
                {"fecha_hora": ["2025-01-27", "09:00"], "profesional": "Gisela", "servicio": "Semi"},
                {"fecha_hora": ["2025-01-27", "10:30"], "profesional": "Gisela", "servicio": "Soft Gel"},
                
                {"fecha_hora": ["2025-01-27", "17:00"], "profesional": "Valentina", "servicio": "Kapping"},
                {"fecha_hora": ["2025-01-27", "18:30"], "profesional": "Valentina", "servicio": "Semi"},
                
                {"fecha_hora": ["2025-01-27", "17:00"], "profesional": "Marisol", "servicio": "Soft Gel"},
                {"fecha_hora": ["2025-01-27", "18:30"], "profesional": "Marisol", "servicio": "Semi"},
                
                {"fecha_hora": ["2025-01-27", "17:00"], "profesional": "Gisela", "servicio": "Semi"},
                {"fecha_hora": ["2025-01-27", "18:30"], "profesional": "Gisela", "servicio": "Kapping"},
            ]
            guardar_turnos(turnos_iniciales)
            logging.info("Archivo de turnos creado con datos iniciales")
            return turnos_iniciales

        with open(ARCHIVO_TURNOS, 'r', encoding='utf-8') as archivo:
            turnos = json.load(archivo)
            logging.info(f"Turnos cargados exitosamente desde {ARCHIVO_TURNOS}")
            return turnos
    except json.JSONDecodeError as e:
        logging.error(f"Error al decodificar JSON: {str(e)}")
        raise
    except Exception as e:
        logging.error(f"Error al cargar turnos: {str(e)}")
        raise
    

def agregar_turno(turno):
    """
    Agrega un nuevo turno.
    """
    try:

        turno_copia = turno.copy()
        if isinstance(turno_copia["fecha_hora"], tuple):
            turno_copia["fecha_hora"] = list(turno_copia["fecha_hora"])
            
        turnos = cargar_turnos()
        turnos.append(turno_copia)
        guardar_turnos(turnos)
        logging.info(f"Nuevo turno agregado: {turno_copia}")
    except Exception as e:
        logging.error(f"Error al agregar turno: {str(e)}")
        raise

def guardar_reservas(reservas):
    """
    Guarda las reservas en un archivo.
    """
    try:
        with open(ARCHIVO_RESERVAS, 'w', encoding='utf-8') as archivo:
            json.dump(reservas, archivo, ensure_ascii=False, indent=4)
        logging.info(f"Reservas guardadas exitosamente en {ARCHIVO_RESERVAS}")
    except Exception as e:
        logging.error(f"Error al guardar reservas: {str(e)}")
        raise

def cargar_reservas():
    """
    Carga las reservas desde un archivo.
    """
    try:
        if not os.path.exists(ARCHIVO_RESERVAS):
            logging.info("Archivo de reservas no encontrado, devolviendo lista vacía")
            return []

        with open(ARCHIVO_RESERVAS, 'r', encoding='utf-8') as archivo:
            reservas = json.load(archivo)
            
            logging.info(f"Reservas cargadas exitosamente desde {ARCHIVO_RESERVAS}")
            return reservas
    except json.JSONDecodeError as e:
        logging.error(f"Error al decodificar JSON de reservas: {str(e)}")
        return [] 
    except Exception as e:
        logging.error(f"Error al cargar reservas: {str(e)}")
        return []
