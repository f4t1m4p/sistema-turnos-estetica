"""
Controlador para funcionalidades de cliente.
Maneja la coordinación entre interfaz y lógica de negocio para clientes.
"""

from sistema_turnos.utils.filtros import filtrar_turnos, filtrar_reservas_por_dni
from sistema_turnos.logica.reservas import (
    confirmar_reserva, crear_reserva, cancelar_reserva,
    procesar_reserva_exitosa, procesar_cancelacion_exitosa
)

class ControladorCliente:
    """
    Controlador que maneja las operaciones específicas de clientes.
    """
    
    def __init__(self, interfaz, turnos, reservas):
        self.interfaz = interfaz
        self.turnos = turnos
        self.reservas = reservas
    
    def filtrar_turnos(self):
        """
        Maneja el filtrado de turnos para clientes.
        FUNCIONALIDAD: Consultar fácilmente qué turnos hay disponibles
        """
        opciones_servicio = ["kapping", "semi", "soft gel"]
        opciones_profesional = ["gisela", "marisol", "valentina"]
        
        # Filtro por servicio
        servicio = self._pedir_filtro_servicio(opciones_servicio)
        if servicio is None:
            return
        
        # Filtro por profesional
        profesional = self._pedir_filtro_profesional(opciones_profesional)
        if profesional is None:
            return
        
        # Aplicar filtros y mostrar resultados
        filtrados = filtrar_turnos(self.turnos, servicio, profesional)
        self.interfaz.mostrar_turnos(filtrados)
    
    def _pedir_filtro_servicio(self, opciones_servicio):
        """
        Pide al usuario que ingrese un filtro de servicio.
        """
        return self.interfaz.pedir_filtro_servicio(opciones_servicio)
    
    def _pedir_filtro_profesional(self, opciones_profesional):
        """
        Pide al usuario que ingrese un filtro de profesional.
        """
        return self.interfaz.pedir_filtro_profesional(opciones_profesional)
    
    def reservar_turno(self):
        """
        Maneja la reserva de turnos para clientes.
        FUNCIONALIDAD: Permitir que las clientas puedan reservar turnos
        """
        resultado = self.interfaz.reservar_turno_columna_lateral(self.turnos)
        if resultado is None:
            return
        
        opcion, nombre, telefono, documento = resultado
        
        try:
            turno = self.turnos[opcion]
            
            # Validar y confirmar reserva
            resultado_validacion = confirmar_reserva(turno, nombre, telefono, documento)
            if not resultado_validacion["valido"]:
                self.interfaz.mostrar_mensaje(resultado_validacion["error"], "error")
                return
            
            if not self.interfaz.confirmar_reserva(turno, nombre, telefono, documento):
                return
            
            # Crear la reserva
            resultado_creacion = crear_reserva(turno, nombre, telefono, documento, self.reservas)
            if not resultado_creacion["exito"]:
                self.interfaz.mostrar_mensaje(resultado_creacion["error"], "error")
                return
            
            # Procesar la reserva exitosa
            resultado_procesamiento = procesar_reserva_exitosa(
                resultado_creacion["reserva"], self.turnos, self.reservas
            )
            
            if resultado_procesamiento["exito"]:
                self.turnos = resultado_procesamiento["turnos_actualizados"]
                self.reservas = resultado_procesamiento["reservas_actualizadas"]
                self.interfaz.mostrar_mensaje("¡Turno reservado exitosamente!", "exito")
            
        except Exception as e:
            self.interfaz.mostrar_mensaje(f"Error al reservar turno: {str(e)}", "error")
    
    def cancelar_turno(self):
        """
        Maneja la cancelación de turnos para clientes.
        FUNCIONALIDAD: Permitir cancelar reservas
        """
        dni = self.interfaz.pedir_dni_cliente()
        if dni is None:
            return
        
        # Buscar reservas del cliente
        reservas_cliente = filtrar_reservas_por_dni(self.reservas, dni)
        if not reservas_cliente:
            self.interfaz.mostrar_mensaje("No se encontraron reservas para este DNI.", "error")
            return
        
        # Mostrar reservas y permitir selección
        reserva_seleccionada = self.interfaz.mostrar_turnos_reservados(reservas_cliente, dni)
        if reserva_seleccionada is None:
            return
        
        # Confirmar cancelación
        if not self.interfaz.confirmar_cancelacion(reserva_seleccionada["turno"], dni):
            return
        
        # Procesar cancelación
        resultado_cancelacion = procesar_cancelacion_exitosa(
            reserva_seleccionada, self.turnos, self.reservas
        )
        
        if resultado_cancelacion["exito"]:
            self.turnos = resultado_cancelacion["turnos_actualizados"]
            self.reservas = resultado_cancelacion["reservas_actualizadas"]
            self.interfaz.mostrar_mensaje("Turno cancelado exitosamente.", "exito")
    
    def ver_turnos_reservados(self):
        """
        Muestra los turnos reservados de un cliente.
        FUNCIONALIDAD: Consultar turnos reservados
        """
        dni = self.interfaz.pedir_dni_cliente()
        if dni is None:
            return
        
        # Buscar reservas del cliente
        reservas_cliente = filtrar_reservas_por_dni(self.reservas, dni)
        if not reservas_cliente:
            self.interfaz.mostrar_mensaje("No se encontraron reservas para este DNI.", "info")
            return
        
        # Mostrar reservas
        self.interfaz.mostrar_turnos_reservados(reservas_cliente, dni) 