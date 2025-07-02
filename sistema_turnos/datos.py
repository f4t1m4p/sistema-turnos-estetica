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

def procesar_turnos_recursivo(turnos_a_procesar, turnos_procesados=None, intentos=0, max_intentos=3):
    """
    Procesa múltiples turnos de forma recursiva.
    
    Args:
        turnos_a_procesar: Lista de turnos a procesar
        turnos_procesados: Lista de turnos ya procesados (para recursión)
        intentos: Número de intentos actuales
        max_intentos: Número máximo de intentos permitidos
    
    Returns:
        Lista de turnos procesados exitosamente
    """
    if turnos_procesados is None:
        turnos_procesados = []
    
   
    if not turnos_a_procesar:
        return turnos_procesados
    
   
    if intentos >= max_intentos:
        logging.warning(f"Se alcanzó el máximo de {max_intentos} intentos al procesar turnos")
        return turnos_procesados
    
    try:
       
        turno_actual = turnos_a_procesar[0]
        turnos_restantes = turnos_a_procesar[1:]
        
        
        agregar_turno(turno_actual)
        turnos_procesados.append(turno_actual)
        
        logging.info(f"Turno procesado exitosamente: {turno_actual}")
        
        
        return procesar_turnos_recursivo(turnos_restantes, turnos_procesados, 0, max_intentos)
        
    except Exception as e:
        logging.error(f"Error procesando turno: {e}")
       
        return procesar_turnos_recursivo(turnos_a_procesar, turnos_procesados, intentos + 1, max_intentos)

def procesar_reservas_recursivo(reservas_a_procesar, reservas_procesadas=None, intentos=0, max_intentos=3):
    """
    Procesa múltiples reservas de forma recursiva.
    
    Args:
        reservas_a_procesar: Lista de reservas a procesar
        reservas_procesadas: Lista de reservas ya procesadas (para recursión)
        intentos: Número de intentos actuales
        max_intentos: Número máximo de intentos permitidos
    
    Returns:
        Lista de reservas procesadas exitosamente
    """
    if reservas_procesadas is None:
        reservas_procesadas = []
    
    
    if not reservas_a_procesar:
        return reservas_procesadas
    
   
    if intentos >= max_intentos:
        logging.warning(f"Se alcanzó el máximo de {max_intentos} intentos al procesar reservas")
        return reservas_procesadas
    
    try:
       
        reserva_actual = reservas_a_procesar[0]
        reservas_restantes = reservas_a_procesar[1:]
        
       
        reservas_existentes = cargar_reservas()
        reservas_existentes.append(reserva_actual)
        guardar_reservas(reservas_existentes)
        
        reservas_procesadas.append(reserva_actual)
        
        logging.info(f"Reserva procesada exitosamente: {reserva_actual['nombre']}")
        
       
        return procesar_reservas_recursivo(reservas_restantes, reservas_procesadas, 0, max_intentos)
        
    except Exception as e:
        logging.error(f"Error procesando reserva: {e}")
       
        return procesar_reservas_recursivo(reservas_a_procesar, reservas_procesadas, intentos + 1, max_intentos)

def validar_turnos_existentes_recursivo(turnos, turnos_validados=None, indice=0):
    """
    Valida todos los turnos existentes de forma recursiva.
    
    Args:
        turnos: Lista de turnos a validar
        turnos_validados: Lista de turnos ya validados (para recursión)
        indice: Índice actual del turno a validar
    
    Returns:
        Lista de turnos validados
    """
    if turnos_validados is None:
        turnos_validados = []
    
    
    if indice >= len(turnos):
        return turnos_validados
    
    try:
        turno_actual = turnos[indice]
        
       
        fecha, hora = turno_actual["fecha_hora"]
        
        
        if not isinstance(fecha, str) or not isinstance(hora, str):
            logging.warning(f"Turno {indice} tiene formato de fecha/hora inválido: {turno_actual}")
          
            return validar_turnos_existentes_recursivo(turnos, turnos_validados, indice + 1)
       
        if not turno_actual.get("profesional") or not turno_actual.get("servicio"):
            logging.warning(f"Turno {indice} tiene datos incompletos: {turno_actual}")
            
            return validar_turnos_existentes_recursivo(turnos, turnos_validados, indice + 1)
        
       
        turnos_validados.append(turno_actual)
        logging.info(f"Turno {indice} validado exitosamente")
        
    except Exception as e:
        logging.error(f"Error validando turno {indice}: {e}")
    
    
    return validar_turnos_existentes_recursivo(turnos, turnos_validados, indice + 1)
