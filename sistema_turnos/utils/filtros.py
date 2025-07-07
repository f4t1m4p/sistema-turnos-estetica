"""
Módulo de filtros para el sistema de turnos.
Contiene funciones para filtrar turnos por diferentes criterios.
"""

def filtrar_turnos(turnos, servicio=None, profesional=None):
    """
    Filtra los turnos por servicio y/o profesional.
    FUNCIONALIDAD: Filtrar información para encontrar rápidamente lo que se busca
    """
    turnos_filtrados = turnos.copy()
    
    if servicio:
        servicio = servicio.lower()
        turnos_filtrados = [t for t in turnos_filtrados if t["servicio"].lower() == servicio]
    
    if profesional:
        profesional = profesional.lower()
        turnos_filtrados = [t for t in turnos_filtrados if t["profesional"].lower() == profesional]
    
    return turnos_filtrados

def filtrar_reservas_por_dni(reservas, dni):
    """
    Filtra las reservas por DNI del cliente.
    FUNCIONALIDAD: Encontrar rápidamente las reservas de un cliente específico
    """
    dni = dni.lower()
    return [r for r in reservas if r["documento"].lower() == dni]

def filtrar_reservas_por_estado(reservas, estado):
    """
    Filtra las reservas por estado (Pendiente, Atendida, No asistió).
    FUNCIONALIDAD: Gestionar reservas según su estado actual
    """
    estado = estado.lower()
    return [r for r in reservas if r["estado"].lower() == estado]

def filtrar_reservas_por_fecha(reservas, fecha):
    """
    Filtra las reservas por fecha específica.
    FUNCIONALIDAD: Ver reservas de un día específico
    """
    return [r for r in reservas if r["turno"]["fecha_hora"][0] == fecha]

def filtrar_reservas_por_profesional(reservas, profesional):
    """
    Filtra las reservas por profesional.
    FUNCIONALIDAD: Ver reservas de un profesional específico
    """
    profesional = profesional.lower()
    return [r for r in reservas if r["turno"]["profesional"].lower() == profesional] 