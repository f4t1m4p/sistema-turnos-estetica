"""
Controlador principal del sistema de turnos.
Coordina los controladores específicos y maneja el flujo principal.
"""

from sistema_turnos.datos.persistencia import cargar_turnos, cargar_reservas
from sistema_turnos.controlador.cliente import ControladorCliente
from sistema_turnos.controlador.manicurista import ControladorManicurista
from sistema_turnos.interfaz.menus import MenusInterfaz
from sistema_turnos.interfaz.pantalla import PantallaInterfaz

class ControladorPrincipal:
    """
    Controlador principal que coordina todos los subsistemas.
    """
    
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.menus = MenusInterfaz(interfaz.stdscr, interfaz.altura, interfaz.ancho)
        self.pantalla = PantallaInterfaz(interfaz.stdscr, interfaz.altura, interfaz.ancho)
        
        # Cargar datos
        self.turnos = cargar_turnos()
        self.reservas = cargar_reservas()
        
        # Inicializar controladores específicos
        self.controlador_cliente = ControladorCliente(interfaz, self.turnos, self.reservas)
        self.controlador_manicurista = ControladorManicurista(interfaz, self.turnos, self.reservas)
    
    def ejecutar(self):
        """
        Método principal que ejecuta el sistema.
        """
        while True:
            opcion = self.menus.mostrar_menu_principal()
            
            if opcion == 0:  # Cliente
                self.ejecutar_menu_cliente()
            elif opcion == 1:  # Manicurista
                self.ejecutar_menu_manicurista()
            elif opcion == 2:  # Salir
                self.pantalla.mostrar_mensaje("Gracias por usar el sistema de turnos. ¡Hasta luego!")
                break
    
    def ejecutar_menu_cliente(self):
        """
        Maneja el menú de cliente.
        """
        while True:
            opcion_cliente = self.menus.menu_cliente()
            
            if opcion_cliente == 0:  # Ver turnos disponibles
                self.pantalla.mostrar_turnos(self.turnos)
            elif opcion_cliente == 1:  # Filtrar turnos
                self.controlador_cliente.filtrar_turnos()
            elif opcion_cliente == 2:  # Reservar turno
                self.controlador_cliente.reservar_turno()
            elif opcion_cliente == 3:  # Cancelar turno
                self.controlador_cliente.cancelar_turno()
            elif opcion_cliente == 4:  # Ver mis turnos reservados
                self.controlador_cliente.ver_turnos_reservados()
            elif opcion_cliente == 5:  # Volver
                break
    
    def ejecutar_menu_manicurista(self):
        """
        Maneja el menú de manicurista.
        """
        while True:
            opcion_manicurista = self.menus.menu_manicurista()
            
            if opcion_manicurista == 0:  # Ver resumen de reservas
                self.controlador_manicurista.mostrar_resumen_reservas()
            elif opcion_manicurista == 1:  # Gestionar reservas pendientes
                self.controlador_manicurista.gestionar_reservas_pendientes()
            elif opcion_manicurista == 2:  # Filtrar reservas por estado
                self.controlador_manicurista.filtrar_turnos()
            elif opcion_manicurista == 3:  # Volver
                break
    
    def actualizar_datos(self):
        """
        Actualiza los datos desde los archivos.
        """
        self.turnos = cargar_turnos()
        self.reservas = cargar_reservas()
        
        # Actualizar referencias en controladores específicos
        self.controlador_cliente.turnos = self.turnos
        self.controlador_cliente.reservas = self.reservas
        self.controlador_manicurista.turnos = self.turnos
        self.controlador_manicurista.reservas = self.reservas 