import os
import curses
from sistema_turnos.datos import cargar_turnos, cargar_reservas, guardar_reservas, guardar_turnos
from sistema_turnos.turnos import mostrar_turnos, filtrar_turnos, reservar_turnos, cancelar_turno
from sistema_turnos.clientes import ver_resumen_reservas, ver_nombre_clientes
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
                    interfaz.reservar_turno_columna_lateral(turnos, solo_vista=True)
                elif opcion_cliente == 1:  
                    servicio = interfaz.pedir_datos_con_esc("Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ")
                    if servicio is None:
                        continue
                    profesional = interfaz.pedir_datos_con_esc("Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ")
                    if profesional is None:
                        continue
                    filtrados = filtrar_turnos(turnos, servicio or None, profesional or None)
                    interfaz.mostrar_turnos(filtrados)
                elif opcion_cliente == 2: 
                    resultado = interfaz.reservar_turno_columna_lateral(turnos)
                    if resultado is None:
                        continue
                    opcion, nombre, telefono, documento = resultado
                    try:
                        turno = turnos[opcion]
                        from sistema_turnos.clientes import validar_documento
                        validar_documento(documento)
                        
                        if any(r["documento"].lower() == documento.lower() for r in reservas):
                            interfaz.mostrar_mensaje("Ya hay un turno reservado con este DNI.", "error")
                            continue
                        
                        if not interfaz.confirmar_reserva(turno, nombre, telefono, documento):
                            continue 
                        cliente = {
                            "nombre": nombre,
                            "telefono": telefono,
                            "documento": documento,
                            "turno": turno,
                            "estado": "Pendiente",
                            "montoCobrado": None
                        }
                        reservas.append(cliente)
                        turnos = [t for t in turnos if t != turno]
                        guardar_reservas(reservas)
                        guardar_turnos(turnos)

                        turnos = cargar_turnos()
                        reservas = cargar_reservas()
                        interfaz.mostrar_mensaje(f"Turno reservado con éxito para {nombre}!", "exito")
                    except (ValueError, IndexError) as e:
                        interfaz.mostrar_mensaje(f"Error: {str(e)}", "error")
                elif opcion_cliente == 3: 
                    documento = interfaz.pedir_datos_con_esc("Ingrese su documento para cancelar el turno: ")
                    if documento is None:
                        continue
                    nuevas_reservas = []
                    turno_recuperado = None
                    for r in reservas:
                        if r["documento"].lower() == documento.lower():
                            turno_recuperado = r["turno"]
                        else:
                            nuevas_reservas.append(r)
                    if turno_recuperado:

                        if interfaz.confirmar_cancelacion(turno_recuperado, documento):
                            turnos.append(turno_recuperado)
                            reservas = nuevas_reservas
                            guardar_reservas(reservas)
                            guardar_turnos(turnos)
                            turnos = cargar_turnos()
                            reservas = cargar_reservas()
                            interfaz.mostrar_mensaje("Turno cancelado correctamente.", "exito")
                        else:
                            interfaz.mostrar_mensaje("Cancelación abortada.", "info")
                    else:
                        interfaz.mostrar_mensaje("No se encontró una reserva con ese documento.", "error")
                elif opcion_cliente == 4:
                    if interfaz.mostrar_turnos_reservados(reservas) is None:
                        continue
                elif opcion_cliente == 5:
                    break
                
        elif opcion == 1:  
            while True:
                opcion_manicurista = interfaz.menu_manicurista()
                
                if opcion_manicurista == 0: 
                    interfaz.mostrar_resumen_reservas(reservas)
                elif opcion_manicurista == 1:  
                    interfaz.gestionar_reservas_pendientes(reservas)
                elif opcion_manicurista == 2:  
                    break
                
        elif opcion == 2: 
            interfaz.mostrar_mensaje("Gracias por usar el sistema de turnos. ¡Hasta luego!", "info")
            break

if __name__ == "__main__":
    curses.wrapper(main)
