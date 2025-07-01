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
                    opciones_servicio = ["kapping", "semi", "soft gel"]
                    opciones_profesional = ["gisela", "marisol", "valentina"]
                    cancelar_filtro = False
                    
                    while True:
                        interfaz.stdscr.clear()
                        interfaz.stdscr.addstr(1, 2, "Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ")
                        interfaz.stdscr.addstr(interfaz.altura - 2, 2, "ESC para volver")
                        if 'error_servicio' in locals() and error_servicio:
                            interfaz.stdscr.attron(curses.color_pair(3))
                            interfaz.stdscr.addstr(2, 2, "Servicio inválido. Opciones: Kapping, Semi, Soft Gel.")
                            interfaz.stdscr.attroff(curses.color_pair(3))
                        interfaz.stdscr.move(3, 2)
                        interfaz.stdscr.clrtoeol()
                        interfaz.stdscr.refresh()
                        curses.echo()
                        buffer = b""
                        while True:
                            ch = interfaz.stdscr.getch(3, 2 + len(buffer))
                            if ch == 27:
                                curses.noecho()
                                cancelar_filtro = True
                                break
                            elif ch in (10, 13):
                                break
                            elif ch in (8, 127):
                                if buffer:
                                    buffer = buffer[:-1]
                                    interfaz.stdscr.move(3, 2 + len(buffer))
                                    interfaz.stdscr.delch()
                            else:
                                buffer += bytes([ch])
                                interfaz.stdscr.addch(3, 2 + len(buffer) - 1, ch)
                        curses.noecho()
                        if cancelar_filtro:
                            break
                        servicio = buffer.decode('utf-8').strip().lower()
                        if servicio == "":
                            servicio = None
                            error_servicio = False
                            break
                        if not servicio.replace(" ", "").isalpha() or servicio not in opciones_servicio:
                            error_servicio = True
                            continue
                        error_servicio = False
                        break
                    if cancelar_filtro:
                        continue
                   
                    while True:
                        interfaz.stdscr.clear()
                        interfaz.stdscr.addstr(1, 2, "Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ")
                        interfaz.stdscr.addstr(interfaz.altura - 2, 2, "ESC para volver")
                        if 'error_prof' in locals() and error_prof:
                            interfaz.stdscr.attron(curses.color_pair(3))
                            interfaz.stdscr.addstr(2, 2, "Profesional inválido. Opciones: Gisela, Marisol, Valentina.")
                            interfaz.stdscr.attroff(curses.color_pair(3))
                        interfaz.stdscr.move(3, 2)
                        interfaz.stdscr.clrtoeol()
                        interfaz.stdscr.refresh()
                        curses.echo()
                        buffer = b""
                        while True:
                            ch = interfaz.stdscr.getch(3, 2 + len(buffer))
                            if ch == 27:
                                curses.noecho()
                                cancelar_filtro = True
                                break
                            elif ch in (10, 13):
                                break
                            elif ch in (8, 127):
                                if buffer:
                                    buffer = buffer[:-1]
                                    interfaz.stdscr.move(3, 2 + len(buffer))
                                    interfaz.stdscr.delch()
                            else:
                                buffer += bytes([ch])
                                interfaz.stdscr.addch(3, 2 + len(buffer) - 1, ch)
                        curses.noecho()
                        if cancelar_filtro:
                            break
                        profesional = buffer.decode('utf-8').strip().lower()
                        if profesional == "":
                            profesional = None
                            error_prof = False
                            break
                        if not profesional.replace(" ", "").isalpha() or profesional not in opciones_profesional:
                            error_prof = True
                            continue
                        error_prof = False
                        break
                    if cancelar_filtro:
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
                    while True:
                        interfaz.stdscr.clear()
                        prompt = "Ingrese su documento para cancelar el turno: "
                        interfaz.stdscr.addstr(1, 2, prompt)
                        interfaz.stdscr.addstr(interfaz.altura - 2, 2, "Presione ESC para volver")
                        if 'error_doc' in locals() and error_doc:
                            interfaz.stdscr.attron(curses.color_pair(3))
                            interfaz.stdscr.addstr(3, 2, "El documento debe contener solo números.")
                            interfaz.stdscr.attroff(curses.color_pair(3))
                        interfaz.stdscr.move(2, 2)
                        interfaz.stdscr.clrtoeol()
                        interfaz.stdscr.refresh()
                        curses.echo()
                        documento = interfaz.stdscr.getstr(2, 2, 20).decode('utf-8').strip()
                        curses.noecho()
                        if documento == "":
                            continue
                        if documento == chr(27):  
                            documento = None
                            break
                        if not documento.isdigit():
                            error_doc = True
                            continue
                        error_doc = False
                        break
                    if documento is None or not documento.isdigit():
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
                    opciones_estado = ["pendiente", "atendido", "no asistió", "no asistio"]
                    opciones_servicio = ["kapping", "semi", "soft gel"]
                    opciones_profesional = ["gisela", "marisol", "valentina"]
                    cancelar_filtro = False
                   
                    while True:
                        interfaz.stdscr.clear()
                        interfaz.stdscr.addstr(1, 2, "Filtrar por estado (Pendiente, Atendido, No asistió o ENTER): ")
                        interfaz.stdscr.addstr(interfaz.altura - 2, 2, "ESC para volver")
                        if 'error_estado' in locals() and error_estado:
                            interfaz.stdscr.attron(curses.color_pair(3))
                            interfaz.stdscr.addstr(2, 2, "Estado inválido. Opciones: Pendiente, Atendido, No asistió.")
                            interfaz.stdscr.attroff(curses.color_pair(3))
                        interfaz.stdscr.move(3, 2)
                        interfaz.stdscr.clrtoeol()
                        interfaz.stdscr.refresh()
                        curses.echo()
                        buffer = b""
                        while True:
                            ch = interfaz.stdscr.getch(3, 2 + len(buffer))
                            if ch == 27:
                                curses.noecho()
                                cancelar_filtro = True
                                break
                            elif ch in (10, 13):
                                break
                            elif ch in (8, 127):
                                if buffer:
                                    buffer = buffer[:-1]
                                    interfaz.stdscr.move(3, 2 + len(buffer))
                                    interfaz.stdscr.delch()
                            else:
                                buffer += bytes([ch])
                                interfaz.stdscr.addch(3, 2 + len(buffer) - 1, ch)
                        curses.noecho()
                        if cancelar_filtro:
                            break
                        estado = buffer.decode('utf-8').strip().lower()
                        if estado == "":
                            estado = None
                            error_estado = False
                            break
                        if not estado.replace(" ", "").isalpha() or estado not in opciones_estado:
                            error_estado = True
                            continue
                        error_estado = False
                        break
                    if cancelar_filtro:
                        continue
                    
                    while True:
                        interfaz.stdscr.clear()
                        interfaz.stdscr.addstr(1, 2, "Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ")
                        interfaz.stdscr.addstr(interfaz.altura - 2, 2, "ESC para volver")
                        if 'error_servicio' in locals() and error_servicio:
                            interfaz.stdscr.attron(curses.color_pair(3))
                            interfaz.stdscr.addstr(2, 2, "Servicio inválido. Opciones: Kapping, Semi, Soft Gel.")
                            interfaz.stdscr.attroff(curses.color_pair(3))
                        interfaz.stdscr.move(3, 2)
                        interfaz.stdscr.clrtoeol()
                        interfaz.stdscr.refresh()
                        curses.echo()
                        buffer = b""
                        while True:
                            ch = interfaz.stdscr.getch(3, 2 + len(buffer))
                            if ch == 27:
                                curses.noecho()
                                cancelar_filtro = True
                                break
                            elif ch in (10, 13):
                                break
                            elif ch in (8, 127):
                                if buffer:
                                    buffer = buffer[:-1]
                                    interfaz.stdscr.move(3, 2 + len(buffer))
                                    interfaz.stdscr.delch()
                            else:
                                buffer += bytes([ch])
                                interfaz.stdscr.addch(3, 2 + len(buffer) - 1, ch)
                        curses.noecho()
                        if cancelar_filtro:
                            break
                        servicio = buffer.decode('utf-8').strip().lower()
                        if servicio == "":
                            servicio = None
                            error_servicio = False
                            break
                        if not servicio.replace(" ", "").isalpha() or servicio not in opciones_servicio:
                            error_servicio = True
                            continue
                        error_servicio = False
                        break
                    if cancelar_filtro:
                        continue
                    
                    while True:
                        interfaz.stdscr.clear()
                        interfaz.stdscr.addstr(1, 2, "Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ")
                        interfaz.stdscr.addstr(interfaz.altura - 2, 2, "ESC para volver")
                        if 'error_prof' in locals() and error_prof:
                            interfaz.stdscr.attron(curses.color_pair(3))
                            interfaz.stdscr.addstr(2, 2, "Profesional inválido. Opciones: Gisela, Marisol, Valentina.")
                            interfaz.stdscr.attroff(curses.color_pair(3))
                        interfaz.stdscr.move(3, 2)
                        interfaz.stdscr.clrtoeol()
                        interfaz.stdscr.refresh()
                        curses.echo()
                        buffer = b""
                        while True:
                            ch = interfaz.stdscr.getch(3, 2 + len(buffer))
                            if ch == 27:
                                curses.noecho()
                                cancelar_filtro = True
                                break
                            elif ch in (10, 13):
                                break
                            elif ch in (8, 127):
                                if buffer:
                                    buffer = buffer[:-1]
                                    interfaz.stdscr.move(3, 2 + len(buffer))
                                    interfaz.stdscr.delch()
                            else:
                                buffer += bytes([ch])
                                interfaz.stdscr.addch(3, 2 + len(buffer) - 1, ch)
                        curses.noecho()
                        if cancelar_filtro:
                            break
                        profesional = buffer.decode('utf-8').strip().lower()
                        if profesional == "":
                            profesional = None
                            error_prof = False
                            break
                        if not profesional.replace(" ", "").isalpha() or profesional not in opciones_profesional:
                            error_prof = True
                            continue
                        error_prof = False
                        break
                    if cancelar_filtro:
                        continue
                    def coincide(r):
                        if estado and r.get('estado', 'Pendiente').lower() != estado:
                            return False
                        if servicio and r['turno']['servicio'].lower() != servicio:
                            return False
                        if profesional and r['turno']['profesional'].lower() != profesional:
                            return False
                        return True
                    filtradas = sorted(filter(coincide, reservas), key=lambda r: (r['turno']['fecha_hora'][0], r['turno']['fecha_hora'][1]))
                    interfaz.mostrar_lista_reservas_navegable(filtradas)
                elif opcion_manicurista == 3:  
                    break
                
        elif opcion == 2: 
            interfaz.mostrar_mensaje("Gracias por usar el sistema de turnos. ¡Hasta luego!", "info")
            break

if __name__ == "__main__":
    curses.wrapper(main)
