import os
from sistema_turnos.datos import cargar_turnos
from sistema_turnos.menu import menu

ENTORNO = os.getenv("ENTORNO", "desarrollo")
if ENTORNO == "produccion":
    print(" Ejecutando en entorno de PRODUCCIÓN")
else:
    print(" Ejecutando en entorno de DESARROLLO")

def main():
    turnos = cargar_turnos()
    reservas = []
    menu(turnos, reservas)

if __name__ == "__main__":
    main()
