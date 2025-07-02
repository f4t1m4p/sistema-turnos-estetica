import os
import curses
from sistema_turnos.interfaz import InterfazTurnos
from sistema_turnos.controlador import ControladorTurnos

ENTORNO = os.getenv("ENTORNO", "desarrollo")

def main(stdscr):
    """
    Función principal del sistema.
    """
    if ENTORNO == "produccion":
        print(" Ejecutando en entorno de PRODUCCIÓN")
    else:
        print(" Ejecutando en entorno de DESARROLLO")

    # Inicia la interfaz y controlador
    interfaz = InterfazTurnos(stdscr)
    controlador = ControladorTurnos(interfaz)
    
    # Ejecuta el sistema
    controlador.ejecutar()

if __name__ == "__main__":
    curses.wrapper(main)
