"""
Controlador para funcionalidades de manicurista.
Maneja la coordinación entre interfaz y lógica de negocio para manicuristas.
"""

from sistema_turnos.utils.filtros import filtrar_reservas_por_estado, filtrar_reservas_por_profesional
from sistema_turnos.logica.atencion import (
    marcar_como_atendida, marcar_como_no_asistio, cambiar_monto_cobrado,
    obtener_estadisticas_reservas, obtener_reservas_pendientes
)

class ControladorManicurista:
    """
    Controlador que maneja las operaciones específicas de manicuristas.
    """
    
    def __init__(self, interfaz, turnos, reservas):
        self.interfaz = interfaz
        self.turnos = turnos
        self.reservas = reservas
    
    def mostrar_resumen_reservas(self):
        """
        Muestra un resumen de todas las reservas y permite seleccionar una para ver detalles.
        FUNCIONALIDAD: Ver estado general de reservas y detalles específicos
        """
        # Mostrar resumen navegable y permitir selección
        reserva_seleccionada = self.interfaz.mostrar_resumen_reservas(self.reservas)
        
        if reserva_seleccionada is not None:
            # Mostrar detalles de la reserva seleccionada
            self.interfaz.mostrar_detalles_reserva(reserva_seleccionada)
    
    def gestionar_reservas_pendientes(self):
        """
        Maneja la gestión de reservas pendientes.
        FUNCIONALIDAD: Gestionar reservas que requieren atención
        """
        reservas_pendientes = obtener_reservas_pendientes(self.reservas)
        
        if not reservas_pendientes:
            self.interfaz.mostrar_mensaje("No hay reservas pendientes.", "info")
            return
        
        # Mostrar lista navegable de reservas
        reserva_seleccionada = self.interfaz.mostrar_lista_reservas_navegable(reservas_pendientes)
        if reserva_seleccionada is None:
            return
        
        # Mostrar opciones para la reserva seleccionada
        self.interfaz.mostrar_opciones_reserva(reserva_seleccionada, self.reservas)
    
    def filtrar_turnos(self):
        """
        Maneja el filtrado de turnos para manicuristas.
        FUNCIONALIDAD: Filtrar información para encontrar rápidamente lo que se busca
        """
        opciones_estado = ["Pendiente", "Atendida", "No asistió"]
        
        # Filtro por estado
        estado = self._pedir_filtro_estado(opciones_estado)
        if estado is None:
            return
        
        # Aplicar filtro y mostrar resultados
        filtradas = filtrar_reservas_por_estado(self.reservas, estado)
        if not filtradas:
            self.interfaz.mostrar_mensaje(f"No hay reservas con estado '{estado}'.", "info")
            return
        
        self.interfaz.mostrar_lista_reservas_navegable(filtradas)
    
    def _pedir_filtro_estado(self, opciones_estado):
        """
        Pide al usuario que ingrese un filtro de estado.
        """
        return self.interfaz.pedir_filtro_estado(opciones_estado)
    
    def marcar_como_atendida(self, reserva):
        """
        Marca una reserva como atendida.
        FUNCIONALIDAD: Registrar que un cliente fue atendido
        """
        resultado = marcar_como_atendida(reserva, self.reservas)
        if resultado["exito"]:
            self.interfaz.mostrar_mensaje(resultado["mensaje"], "exito")
        else:
            self.interfaz.mostrar_mensaje(resultado["error"], "error")
    
    def marcar_como_no_asistio(self, reserva):
        """
        Marca una reserva como no asistió.
        FUNCIONALIDAD: Registrar que un cliente no asistió
        """
        resultado = marcar_como_no_asistio(reserva, self.reservas)
        if resultado["exito"]:
            self.interfaz.mostrar_mensaje(resultado["mensaje"], "exito")
        else:
            self.interfaz.mostrar_mensaje(resultado["error"], "error")
    
    def cambiar_monto_cobrado(self, reserva):
        """
        Cambia el monto cobrado por un servicio.
        FUNCIONALIDAD: Registrar el monto cobrado por un servicio
        """
        monto = self.interfaz.pedir_monto_cobrado()
        if monto is None:
            return
        
        resultado = cambiar_monto_cobrado(reserva, monto, self.reservas)
        if resultado["exito"]:
            self.interfaz.mostrar_mensaje(resultado["mensaje"], "exito")
        else:
            self.interfaz.mostrar_mensaje(resultado["error"], "error")
    
    def mostrar_estadisticas(self):
        """
        Muestra estadísticas de las reservas.
        FUNCIONALIDAD: Generar reportes y estadísticas
        """
        stats = obtener_estadisticas_reservas(self.reservas)
        self.interfaz.mostrar_estadisticas(stats) 