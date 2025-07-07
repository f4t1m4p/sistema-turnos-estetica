"""
Punto de entrada principal del sistema de turnos.
"""

import curses
from sistema_turnos.interfaz import InterfazTurnos
from sistema_turnos.controlador_principal import ControladorPrincipal

def main(stdscr):
    """
    Función principal que inicializa y ejecuta el sistema.
    """
    try:
        # Inicializar interfaz
        interfaz = InterfazTurnos(stdscr)
        
        # Verificar tamaño de pantalla
        if interfaz.ancho < interfaz.tamanio_minimo_ancho or interfaz.altura < interfaz.tamanio_minimo_altura:
            return
        
        # Inicializar controlador principal
        controlador = ControladorPrincipal(interfaz)
        
        # Ejecutar sistema
        controlador.ejecutar()
        
    except KeyboardInterrupt:
        # Manejar interrupción del usuario
        pass
    except Exception as e:
        # Manejar errores inesperados
        stdscr.clear()
        stdscr.addstr(1, 2, f"Error inesperado: {str(e)}")
        stdscr.addstr(3, 2, "Presiona cualquier tecla para salir...")
        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    # Ejecutar el sistema con curses
    curses.wrapper(main)
