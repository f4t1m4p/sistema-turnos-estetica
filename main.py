import os
import curses
from sistema_turnos.datos import cargar_turnos, cargar_reservas, guardar_reservas, guardar_turnos
from sistema_turnos.turnos import mostrar_turnos, filtrar_turnos, reservar_turnos, cancelar_turno
from sistema_turnos.clientes import ver_resumen_reservas, ver_nombre_clientes, ver_servicios_y_profesionales
from sistema_turnos.interfaz import InterfazTurnos

ENTORNO = os.getenv("ENTORNO", "desarrollo")

def main(stdscr):
    """
    Función principal del sistema.
    """
    if ENTORNO == "produccion":
        print(" Ejecutando en entorno de PRODUCCIÓN")
    else:
        print(" Ejecutando en entorno de DESARROLLO")

    interfaz = InterfazTurnos(stdscr)
    turnos = cargar_turnos()
    reservas = cargar_reservas()

    while True:
        opcion = interfaz.mostrar_menu_principal()
        
        if opcion == 0: 
            while True:
                opcion_cliente = interfaz.menu_cliente()
                
                if opcion_cliente == 0:  
                    interfaz.mostrar_turnos(turnos)
                elif opcion_cliente == 1:  
                    servicio = interfaz.pedir_datos("Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ")
                    profesional = interfaz.pedir_datos("Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ")
                    filtrados = filtrar_turnos(turnos, servicio or None, profesional or None)
                    interfaz.mostrar_turnos(filtrados)
                elif opcion_cliente == 2: 
                    interfaz.mostrar_turnos(turnos)
                    try:
                        opcion = int(interfaz.pedir_datos("Elija el número del turno que desea reservar: ")) - 1
                        turno = turnos[opcion]
                        nombre = interfaz.pedir_datos("Ingrese su nombre: ")
                        telefono = interfaz.pedir_datos("Ingrese su teléfono: ")
                        documento = interfaz.pedir_datos("Ingrese su documento: ")
                        
                        from sistema_turnos.clientes import validar_documento
                        validar_documento(documento)
                        
                        cliente = {
                            "nombre": nombre,
                            "telefono": telefono,
                            "documento": documento,
                            "turno": turno,
                        }
                        reservas.append(cliente)
                        turnos = [t for t in turnos if t != turno]
                        guardar_reservas(reservas)
                        guardar_turnos(turnos)
                        interfaz.mostrar_mensaje(f"Turno reservado con éxito para {nombre}!", "exito")
                    except (ValueError, IndexError) as e:
                        interfaz.mostrar_mensaje(f"Error: {str(e)}", "error")
                elif opcion_cliente == 3: 
                    documento = interfaz.pedir_datos("Ingrese su documento para cancelar el turno: ")
                    nuevas_reservas = []
                    turno_recuperado = None
                    
                    for r in reservas:
                        if r["documento"].lower() == documento.lower():
                            turno_recuperado = r["turno"]
                            interfaz.mostrar_mensaje("Turno cancelado correctamente.", "exito")
                        else:
                            nuevas_reservas.append(r)
                    
                    if turno_recuperado:
                        turnos.append(turno_recuperado)
                    else:
                        interfaz.mostrar_mensaje("No se encontró una reserva con ese documento.", "error")
                    
                    reservas = nuevas_reservas
                    guardar_reservas(reservas)
                    guardar_turnos(turnos)
                elif opcion_cliente == 4: 
                    servicios = set(t["servicio"] for t in turnos)
                    profesionales = set(t["profesional"] for t in turnos)
                    interfaz.mostrar_mensaje(f"Servicios: {', '.join(servicios)}\nProfesionales: {', '.join(profesionales)}", "info")
                elif opcion_cliente == 5:  
                    break
                
        elif opcion == 1:  
            while True:
                opcion_manicurista = interfaz.menu_manicurista()
                
                if opcion_manicurista == 0: 
                    interfaz.mostrar_resumen_reservas(reservas)
                elif opcion_manicurista == 1:  
                    nombres = {r["nombre"] for r in reservas}
                    interfaz.mostrar_mensaje("Clientes con turnos reservados:\n" + "\n".join(f"- {nombre}" for nombre in nombres), "info")
                elif opcion_manicurista == 2:  
                    break
                
        elif opcion == 2: 
            interfaz.mostrar_mensaje("Gracias por usar el sistema de turnos. ¡Hasta luego!", "info")
            break

if __name__ == "__main__":
    curses.wrapper(main)
