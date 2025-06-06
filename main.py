import os
from sistema_turnos.datos import cargar_turnos, cargar_reservas
from sistema_turnos.menu import menu

ENTORNO = os.getenv("ENTORNO", "desarrollo")
if ENTORNO == "produccion":
    print(" Ejecutando en entorno de PRODUCCIÓN")
else:
    print(" Ejecutando en entorno de DESARROLLO")

def main():
    turnos = cargar_turnos()
    reservas = cargar_reservas() 
    rol = None
    while rol not in ["cliente", "manicurista"]:
        rol_input = input("¿Eres 'cliente' o 'manicurista'? ").lower().strip()
        if rol_input in ["cliente", "manicurista"]:
            rol = rol_input
        else:
            print("Rol inválido. Por favor, ingresa 'cliente' o 'manicurista'.")

    menu(turnos, reservas, rol)

if __name__ == "__main__":
    main()
