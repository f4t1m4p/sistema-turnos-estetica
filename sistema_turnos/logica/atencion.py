"""
Módulo de lógica de negocio para atención.
Contiene las reglas de negocio para gestionar la atención de clientes.
"""

from sistema_turnos.datos.persistencia import guardar_reservas

def marcar_como_atendida(reserva, reservas):
    """
    Marca una reserva como atendida.
    FUNCIONALIDAD: Registrar que un cliente fue atendido
    """
    if reserva in reservas:
        reserva["estado"] = "Atendida"
        guardar_reservas(reservas)
        return {
            "exito": True,
            "mensaje": f"Cliente {reserva['nombre']} marcado como atendido."
        }
    return {
        "exito": False,
        "error": "Reserva no encontrada."
    }

def marcar_como_no_asistio(reserva, reservas):
    """
    Marca una reserva como no asistió.
    FUNCIONALIDAD: Registrar que un cliente no asistió
    """
    if reserva in reservas:
        reserva["estado"] = "No asistió"
        guardar_reservas(reservas)
        return {
            "exito": True,
            "mensaje": f"Cliente {reserva['nombre']} marcado como no asistió."
        }
    return {
        "exito": False,
        "error": "Reserva no encontrada."
    }

def cambiar_monto_cobrado(reserva, monto, reservas):
    """
    Cambia el monto cobrado por un servicio.
    FUNCIONALIDAD: Registrar el monto cobrado por un servicio
    """
    try:
        monto_float = float(monto)
        if monto_float < 0:
            return {
                "exito": False,
                "error": "El monto no puede ser negativo."
            }
        
        if reserva in reservas:
            reserva["montoCobrado"] = monto_float
            guardar_reservas(reservas)
            return {
                "exito": True,
                "mensaje": f"Monto actualizado: ${monto_float:.2f}"
            }
        return {
            "exito": False,
            "error": "Reserva no encontrada."
        }
    except ValueError:
        return {
            "exito": False,
            "error": "El monto debe ser un número válido."
        }

def obtener_estadisticas_reservas(reservas):
    """
    Obtiene estadísticas de las reservas.
    FUNCIONALIDAD: Generar reportes y estadísticas
    """
    total_reservas = len(reservas)
    pendientes = len([r for r in reservas if r["estado"] == "Pendiente"])
    atendidas = len([r for r in reservas if r["estado"] == "Atendida"])
    no_asistieron = len([r for r in reservas if r["estado"] == "No asistió"])
    
    # Calcular ingresos totales
    ingresos_totales = sum(r["montoCobrado"] or 0 for r in reservas)
    
    # Estadísticas por profesional
    stats_profesional = {}
    for reserva in reservas:
        prof = reserva["turno"]["profesional"]
        if prof not in stats_profesional:
            stats_profesional[prof] = {"total": 0, "atendidas": 0, "ingresos": 0}
        
        stats_profesional[prof]["total"] += 1
        if reserva["estado"] == "Atendida":
            stats_profesional[prof]["atendidas"] += 1
            stats_profesional[prof]["ingresos"] += reserva["montoCobrado"] or 0
    
    return {
        "total_reservas": total_reservas,
        "pendientes": pendientes,
        "atendidas": atendidas,
        "no_asistieron": no_asistieron,
        "ingresos_totales": ingresos_totales,
        "por_profesional": stats_profesional
    }

def obtener_reservas_pendientes(reservas):
    """
    Obtiene las reservas pendientes ordenadas por fecha.
    FUNCIONALIDAD: Gestionar reservas que requieren atención
    """
    pendientes = [r for r in reservas if r["estado"] == "Pendiente"]
    
    # Ordenar por fecha y hora
    pendientes.sort(key=lambda x: (x["turno"]["fecha_hora"][0], x["turno"]["fecha_hora"][1]))
    
    return pendientes 