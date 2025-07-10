"""
Módulo de lógica de negocio para reservas.
Contiene las reglas de negocio para gestionar reservas de turnos.
"""

from sistema_turnos.utils.validaciones import (
    validar_documento, validar_telefono, validar_nombre
)
from sistema_turnos.utils.filtros import filtrar_reservas_por_dni
from sistema_turnos.datos.persistencia import guardar_reservas, guardar_turnos

def confirmar_reserva(turno, nombre, telefono, documento):
    """
    Valida y confirma una reserva de turno.
    FUNCIONALIDAD: Validar datos antes de confirmar una reserva
    """
    # Validar cada campo por separado para dar mensajes más específicos
    try:
        nombre_valido = validar_nombre(nombre)
    except ValueError as e:
        return {
            "valido": False,
            "error": f"Error en el nombre: {str(e)}"
        }
    
    try:
        telefono_valido = validar_telefono(telefono)
    except ValueError as e:
        return {
            "valido": False,
            "error": f"Error en el teléfono: {str(e)}"
        }
    
    try:
        documento_valido = validar_documento(documento)
    except ValueError as e:
        return {
            "valido": False,
            "error": f"Error en el DNI: {str(e)}"
        }
    
    return {
        "turno": turno,
        "nombre": nombre_valido,
        "telefono": telefono_valido,
        "documento": documento_valido,
        "valido": True
    }

def crear_reserva(turno, nombre, telefono, documento, reservas):
    """
    Crea una nueva reserva y la agrega a la lista.
    FUNCIONALIDAD: Crear y almacenar una nueva reserva
    """
    # Verificar que no haya reserva previa con el mismo DNI
    if any(r["documento"].lower() == documento.lower() for r in reservas):
        return {
            "exito": False,
            "error": "Ya hay un turno reservado con este DNI."
        }
    
    # Crear nueva reserva
    nueva_reserva = {
        "nombre": nombre,
        "telefono": telefono,
        "documento": documento,
        "turno": turno,
        "estado": "Pendiente",
        "montoCobrado": None
    }
    
    return {
        "exito": True,
        "reserva": nueva_reserva
    }

def cancelar_reserva(documento, turno, reservas):
    """
    Cancela una reserva existente.
    FUNCIONALIDAD: Permitir cancelar reservas
    """
    # Buscar la reserva
    reserva_encontrada = None
    for reserva in reservas:
        if (reserva["documento"].lower() == documento.lower() and 
            reserva["turno"]["fecha_hora"] == turno["fecha_hora"] and
            reserva["turno"]["profesional"] == turno["profesional"] and
            reserva["turno"]["servicio"] == turno["servicio"]):
            reserva_encontrada = reserva
            break
    
    if not reserva_encontrada:
        return {
            "exito": False,
            "error": "No se encontró la reserva especificada."
        }
    
    return {
        "exito": True,
        "reserva": reserva_encontrada
    }

def procesar_reserva_exitosa(reserva, turnos, reservas):
    """
    Procesa una reserva exitosa actualizando los datos.
    FUNCIONALIDAD: Actualizar datos después de una reserva exitosa
    """
    # Agregar la reserva
    reservas.append(reserva)
    
    # Remover el turno de los disponibles
    turnos = [t for t in turnos if t != reserva["turno"]]
    
    # Guardar cambios
    guardar_reservas(reservas)
    guardar_turnos(turnos)
    
    return {
        "exito": True,
        "turnos_actualizados": turnos,
        "reservas_actualizadas": reservas
    }

def procesar_cancelacion_exitosa(reserva, turnos, reservas):
    """
    Procesa una cancelación exitosa actualizando los datos.
    FUNCIONALIDAD: Actualizar datos después de una cancelación exitosa
    """
    # Remover la reserva
    reservas.remove(reserva)
    
    # Devolver el turno a los disponibles
    turnos.append(reserva["turno"])
    
    # Guardar cambios
    guardar_reservas(reservas)
    guardar_turnos(turnos)
    
    return {
        "exito": True,
        "turnos_actualizados": turnos,
        "reservas_actualizadas": reservas
    } 