import json
import os
from datetime import datetime
import logging


logging.basicConfig(
    filename='sistema_turnos.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ARCHIVO_TURNOS = "turnos.json"
ARCHIVO_RESERVAS = "reservas.json"

def guardar_turnos(turnos):
    """
    Guarda la lista de turnos en un archivo JSON.
    
    Args:
        turnos (list): Lista de diccionarios con la información de los turnos
    """
    try:
        # Convertir tuplas a listas para serialización JSON
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
    Carga los turnos desde el archivo JSON.
    Si el archivo no existe, crea uno con turnos iniciales.
    
    Returns:
        list: Lista de diccionarios con la información de los turnos
    """
    try:
        if not os.path.exists(ARCHIVO_TURNOS):
            turnos_iniciales = [
                {"fecha_hora": ["2025-04-26", "10:00"], "profesional": "Gisela", "servicio": "Kapping"},
                {"fecha_hora": ["2025-04-25", "14:00"], "profesional": "Marisol", "servicio": "Semi"},
                {"fecha_hora": ["2025-04-26", "16:00"], "profesional": "Valentina", "servicio": "Soft Gel"},
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
    Agrega un nuevo turno al archivo.
    
    Args:
        turno (dict): Diccionario con la información del nuevo turno
    """
    try:
        # Convertir tupla a lista si es necesario
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
    Guarda la lista de reservas en un archivo JSON.
    
    Args:
        reservas (list): Lista de diccionarios con la información de las reservas
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
    Carga las reservas desde el archivo JSON.
    Si el archivo no existe, devuelve una lista vacía.
    
    Returns:
        list: Lista de diccionarios con la información de las reservas
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
        # Dependiendo del requisito, podrías querer lanzar la excepción o devolver una lista vacía/manejar el error
        return [] # Devolvemos lista vacía si hay un error de formato para no detener el programa
    except Exception as e:
        logging.error(f"Error al cargar reservas: {str(e)}")
        return []
