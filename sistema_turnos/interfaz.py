"""
Interfaz de usuario del sistema de turnos.
"""

import curses
import time
from datetime import datetime

class InterfazTurnos:
    """
    Clase que maneja la interfaz de usuario.
    """
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.altura, self.ancho = stdscr.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
        curses.curs_set(0)  
        
        self.stdscr.keypad(True) 
        curses.noecho()  
        curses.cbreak() 

    def mostrar_titulo(self, titulo):
        """
        Muestra un título en la pantalla.
        """
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len(titulo)) // 2, titulo)
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()

    def mostrar_menu_principal(self):
        """
        Muestra el menú principal.
        """
        self.mostrar_titulo("SISTEMA DE TURNOS")
        opciones = ["Cliente", "Manicurista", "Salir"]
        return self.menu_seleccion(opciones, 3)

    def menu_seleccion(self, opciones, inicio_y):
        """
        Maneja la selección en un menú.
        """
        seleccion = 0
        while True:
            
            for y in range(inicio_y, inicio_y + len(opciones)):
                self.stdscr.move(y, 0)
                self.stdscr.clrtoeol()

            
            for idx, opcion in enumerate(opciones):
                y = inicio_y + idx
                if y < self.altura - 1:  
                    if idx == seleccion:
                        self.stdscr.attron(curses.color_pair(2))
                        self.stdscr.addstr(y, (self.ancho - len(opcion)) // 2, f"> {opcion}")
                        self.stdscr.attroff(curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y, (self.ancho - len(opcion)) // 2, f"  {opcion}")

            self.stdscr.refresh()
            tecla = self.stdscr.getch()

            
            if tecla == curses.KEY_UP:
                seleccion = max(0, seleccion - 1)
            elif tecla == curses.KEY_DOWN:
                seleccion = min(len(opciones) - 1, seleccion + 1)
            elif tecla == 10:  
                return seleccion
            elif tecla == 27:  
                return -1

    def mostrar_turnos(self, turnos):
        """
        Muestra los turnos disponibles con colores.
        """
        self.stdscr.clear()
        # Título celeste
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len("TURNOS DISPONIBLES")) // 2, "TURNOS DISPONIBLES")
        self.stdscr.attroff(curses.color_pair(1))
        y = 3
        for i, turno in enumerate(turnos):
            if y < self.altura - 1:
                fecha, hora = turno["fecha_hora"]
                texto = f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}"
                self.stdscr.addstr(y, 2, texto)
                y += 1
        # Mensaje de ayuda amarillo
        self.stdscr.move(self.altura - 2, 0)
        self.stdscr.clrtoeol()
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(self.altura - 2, 2, "Presione ENTER para continuar...")
        self.stdscr.attroff(curses.color_pair(4))
        self.stdscr.refresh()
        while True:
            tecla = self.stdscr.getch()
            if tecla == 10:  
                break

    def mostrar_mensaje(self, mensaje, tipo="info"):
        """
        Muestra un mensaje al usuario y espera ENTER para continuar.
        """
        self.stdscr.clear()
        color = {
            "error": 3,
            "info": 4,
            "exito": 2
        }.get(tipo, 4)
        self.stdscr.attron(curses.color_pair(color))
        self.stdscr.addstr(self.altura // 2, (self.ancho - len(mensaje)) // 2, mensaje)
        self.stdscr.attroff(curses.color_pair(color))
    
        texto_enter = "Presione ENTER para volver al inicio..."
        self.stdscr.attron(curses.A_DIM)
        self.stdscr.addstr(self.altura // 2 + 2, (self.ancho - len(texto_enter)) // 2, texto_enter)
        self.stdscr.attroff(curses.A_DIM)
        self.stdscr.refresh()
        while True:
            tecla = self.stdscr.getch()
            if tecla == 10:  
                break

    def pedir_datos(self, prompt):
        """
        Pide datos al usuario, permite volver con ESC.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, prompt)
        self.stdscr.addstr(self.altura - 2, 2, "Presione ESC para volver")
        self.stdscr.refresh()
        curses.echo()
        datos = ""
        while True:
            datos = self.stdscr.getstr(2, 2).decode('utf-8')
            if datos == "":

                continue
            break
        curses.noecho()
        return datos

    def pedir_datos_con_esc(self, prompt):
        """
        Pide datos al usuario, permite volver con ESC.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, prompt)
        self.stdscr.addstr(self.altura - 2, 2, "Presione ESC para volver")
        self.stdscr.refresh()
        curses.echo()
        buffer = b""
        while True:
            ch = self.stdscr.getch(2, 2 + len(buffer))
            if ch == 27:  
                curses.noecho()
                return None
            elif ch in (10, 13): 
                break
            elif ch in (8, 127):  
                if buffer:
                    buffer = buffer[:-1]
                    self.stdscr.move(2, 2 + len(buffer))
                    self.stdscr.delch()
            else:
                buffer += bytes([ch])
                self.stdscr.addch(2, 2 + len(buffer) - 1, ch)
        curses.noecho()
        return buffer.decode('utf-8')

    def menu_cliente(self):
        """
        Muestra el menú de cliente.
        """
        self.stdscr.clear()
        self.stdscr.refresh()
        opciones = [
            "Ver turnos disponibles",
            "Filtrar turnos",
            "Reservar turno",
            "Cancelar turno",
            "Ver mis turnos reservados",
            "Volver"
        ]
        return self.menu_seleccion(opciones, 3)

    def menu_manicurista(self):
        """
        Muestra el menú de manicurista.
        """
        self.stdscr.clear()
        self.stdscr.refresh()
        opciones = [
            "Ver resumen de reservas",
            "Volver"
        ]
        return self.menu_seleccion(opciones, 3)

    def mostrar_resumen_reservas(self, reservas):
        """
        Muestra un resumen de las reservas con colores.
        """
   
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len("RESUMEN DE RESERVAS")) // 2, "RESUMEN DE RESERVAS")
        self.stdscr.attroff(curses.color_pair(1))
        y = 4
        resumen = {}
        for r in reservas:
            profesional = r["turno"]["profesional"]
            resumen.setdefault(profesional, []).append(r)
        for profesional, lista in resumen.items():
            if y < self.altura - 1:
                self.stdscr.attron(curses.color_pair(2))
                self.stdscr.addstr(y, 2, f"Turnos de {profesional}:")
                self.stdscr.attroff(curses.color_pair(2))
                y += 1
                for r in lista:
                    if y < self.altura - 1:
                        fecha, hora = r["turno"]["fecha_hora"]
                        texto = f"- {r['nombre']} el {fecha} a las {hora} para {r['turno']['servicio']}"
                        self.stdscr.addstr(y, 4, texto)
                        y += 1
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(self.altura - 2, 2, f"Total de reservas: {len(reservas)}")
        self.stdscr.addstr(self.altura - 1, 2, "Presione ENTER para continuar...")
        self.stdscr.attroff(curses.color_pair(4))
        self.stdscr.refresh()
        while True:
            tecla = self.stdscr.getch()
            if tecla == 10:
                break

    def mostrar_turnos_reservados(self, reservas):
        """
        Pide DNI y muestra los turnos reservados para ese documento. Permite volver con ESC.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, "Ingrese su DNI para ver sus turnos reservados:")
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(self.altura - 2, 2, "Presione ESC para volver")
        self.stdscr.attroff(curses.color_pair(4))
        self.stdscr.refresh()
        curses.echo()
        dni = self.pedir_datos_con_esc("Ingrese su DNI para ver sus turnos reservados:")
        if dni is None:
            return None
        curses.noecho()
        self.stdscr.clear()
        self.stdscr.addstr(1, (self.ancho - len("MIS TURNOS RESERVADOS")) // 2, "MIS TURNOS RESERVADOS")
        y = 4
        encontrados = False
        if not dni or dni.strip() == "":
            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(y, 2, "No ingresó un DNI válido.")
            self.stdscr.attroff(curses.color_pair(3))
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 2, 2, "Presione ESC para volver")
            self.stdscr.attroff(curses.color_pair(4))
            self.stdscr.refresh()
            while True:
                tecla = self.stdscr.getch()
                if tecla == 27 or tecla == 10:
                    return None
        for r in reservas:
            if r["documento"].strip().lower() == dni.strip().lower():
                fecha, hora = r["turno"]["fecha_hora"]
                texto = f"- {fecha} {hora} - {r['turno']['servicio']} con {r['turno']['profesional']}"
                self.stdscr.addstr(y, 2, texto)
                y += 1
                encontrados = True
        if not encontrados:
            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(y, 2, "No se encontraron turnos reservados para ese DNI.")
            self.stdscr.attroff(curses.color_pair(3))
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(self.altura - 2, 2, "Presione ESC para volver")
        self.stdscr.attroff(curses.color_pair(4))
        self.stdscr.refresh()
        while True:
            tecla = self.stdscr.getch()
            if tecla == 27 or tecla == 10:
                return None

    def mostrar_ventana_turnos_libres(self, turnos):
        """
        Muestra una ventana flotante con los turnos disponibles.
        """
        alto = min(15, self.altura - 4)
        ancho = min(60, self.ancho - 4)
        win = curses.newwin(alto, ancho, 2, (self.ancho - ancho) // 2)
        win.box()
        win.addstr(1, 2, "TURNOS DISPONIBLES:")
        y = 3
        for i, turno in enumerate(turnos):
            if y < alto - 2:
                fecha, hora = turno["fecha_hora"]
                texto = f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}"
                win.addstr(y, 2, texto)
                y += 1
        win.addstr(alto - 2, 2, "Presione ENTER para continuar...")
        win.refresh()
        while True:
            tecla = win.getch()
            if tecla == 10: 
                break
        del win
        self.stdscr.touchwin()
        self.stdscr.refresh()

    def reservar_turno_columna_lateral(self, turnos, solo_vista=False):
        """
        Muestra los turnos a la izquierda con scroll y el formulario de reserva a la derecha.
        Si solo_vista=True, solo permite visualizar y navegar, sin reservar.
        Devuelve (opcion, nombre, telefono, documento) o None si cancela o si solo_vista.
        """
        self.stdscr.clear()

        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, 2, "TURNOS DISPONIBLES:")
        self.stdscr.attroff(curses.color_pair(1))
        ancho_turnos = int(self.ancho * 0.65)
        ancho_form = self.ancho - ancho_turnos - 4
        max_turnos_vista = self.altura - 7  
        scroll = 0
        seleccion = 0
        while True:
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(1, 2, "TURNOS DISPONIBLES:")
            self.stdscr.attroff(curses.color_pair(1))
            y = 3
            turnos_vista = turnos[scroll:scroll+max_turnos_vista]
            for idx, turno in enumerate(turnos_vista):
                if y < self.altura - 3:
                    fecha, hora = turno["fecha_hora"]
                    texto = f"{scroll+idx+1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}"
                    if scroll+idx == seleccion:
                        self.stdscr.attron(curses.color_pair(2))
                        self.stdscr.addstr(y, 2, texto[:ancho_turnos-4])
                        self.stdscr.attroff(curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y, 2, texto[:ancho_turnos-4])
                    y += 1

            self.stdscr.attron(curses.color_pair(4))
            if solo_vista:
                self.stdscr.addstr(self.altura - 3, 2, "↑↓ para navegar, ESC para volver")
            else:
                self.stdscr.addstr(self.altura - 3, 2, "↑↓ para navegar, ENTER para elegir, ESC para cancelar")
            self.stdscr.attroff(curses.color_pair(4))
           
            x_form = ancho_turnos + 4
            if not solo_vista:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(1, x_form, "RESERVAR TURNO:")
                self.stdscr.attroff(curses.color_pair(1))
            self.stdscr.refresh()
            tecla = self.stdscr.getch()
            if tecla == curses.KEY_UP and seleccion > 0:
                seleccion -= 1
                if seleccion < scroll:
                    scroll -= 1
            elif tecla == curses.KEY_DOWN and seleccion < len(turnos) - 1:
                seleccion += 1
                if seleccion >= scroll + max_turnos_vista:
                    scroll += 1
            elif solo_vista:
                if tecla == 27:  
                    return None

            else:
                if tecla == 10:  
                    break
                elif tecla == 27:  
                    return None

        self.stdscr.move(self.altura - 3, 0)
        self.stdscr.clrtoeol()
        if solo_vista:
            return None

        fila_max = self.altura - 2 if self.altura - 2 > 13 else self.altura - 2
        fila_error = self.altura - 2
        ancho_max = self.ancho - x_form - 1
        while True:
            curses.echo()
            self.stdscr.addstr(5, x_form, "Nombre:")
            self.stdscr.move(6, x_form)
            self.stdscr.clrtoeol()
            nombre = self.stdscr.getstr(6, x_form, 30).decode('utf-8').strip()
            self.stdscr.move(fila_error, 0)
            self.stdscr.clrtoeol()
            if not nombre.isalpha():
                mensaje = "Solo letras."
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(fila_error, x_form, mensaje[:ancho_max])
                self.stdscr.attroff(curses.color_pair(3))
                self.stdscr.refresh()
                curses.napms(1200)
                self.stdscr.move(fila_error, 0)
                self.stdscr.clrtoeol()
                self.stdscr.move(6, x_form)
                self.stdscr.clrtoeol()
                continue
            break
        while True:
            self.stdscr.addstr(8, x_form, "Teléfono:")
            self.stdscr.move(9, x_form)
            self.stdscr.clrtoeol()
            telefono = self.stdscr.getstr(9, x_form, 20).decode('utf-8').strip()
            self.stdscr.move(fila_error, 0)
            self.stdscr.clrtoeol()
            if not telefono.isdigit():
                mensaje = "Solo números."
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(fila_error, x_form, mensaje[:ancho_max])
                self.stdscr.attroff(curses.color_pair(3))
                self.stdscr.refresh()
                curses.napms(1200)
                self.stdscr.move(fila_error, 0)
                self.stdscr.clrtoeol()
                self.stdscr.move(9, x_form)
                self.stdscr.clrtoeol()
                continue
            break
        while True:
            self.stdscr.addstr(11, x_form, "Documento:")
            self.stdscr.move(12, x_form)
            self.stdscr.clrtoeol()
            documento = self.stdscr.getstr(12, x_form, 20).decode('utf-8').strip()
            self.stdscr.move(fila_error, 0)
            self.stdscr.clrtoeol()
            if not documento.isdigit():
                mensaje = "DNI: solo números."
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(fila_error, x_form, mensaje[:ancho_max])
                self.stdscr.attroff(curses.color_pair(3))
                self.stdscr.refresh()
                curses.napms(1200)
                self.stdscr.move(fila_error, 0)
                self.stdscr.clrtoeol()
                self.stdscr.move(12, x_form)
                self.stdscr.clrtoeol()
                continue
            break
        curses.noecho()
        return seleccion, nombre, telefono, documento

    def confirmar_reserva(self, turno, nombre, telefono, documento):
        """
        Muestra un resumen de la reserva y pide confirmación.
        Devuelve True si confirma, False si quiere volver a empezar.
        """
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.mostrar_titulo("CONFIRMAR RESERVA")
        self.stdscr.attroff(curses.color_pair(1))
        y = 4
        self.stdscr.addstr(y, 4, f"Nombre: {nombre}")
        self.stdscr.addstr(y+1, 4, f"Teléfono: {telefono}")
        self.stdscr.addstr(y+2, 4, f"Documento: {documento}")
        fecha, hora = turno["fecha_hora"]
        self.stdscr.addstr(y+3, 4, f"Turno: {fecha} {hora} - {turno['servicio']} con {turno['profesional']}")
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(y+5, 4, "¿Está seguro que quiere reservar este turno? (si/no)")
        self.stdscr.attroff(curses.color_pair(4))
        self.stdscr.refresh()
        curses.echo()
        while True:
            self.stdscr.move(y+6, 4)
            self.stdscr.clrtoeol()
            respuesta = self.stdscr.getstr(y+6, 4, 5).decode('utf-8').strip().lower()
            if respuesta.replace(' ', '') == "si":
                curses.noecho()
                return True
            elif respuesta.replace(' ', '') == "no":
                curses.noecho()
                return False
        curses.noecho()

    def confirmar_cancelacion(self, turno, documento):
        """
        Muestra un resumen del turno a cancelar y pide confirmación.
        Devuelve True si confirma, False si cancela la operación.
        """
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.mostrar_titulo("CONFIRMAR CANCELACIÓN")
        self.stdscr.attroff(curses.color_pair(1))
        y = 4
        self.stdscr.addstr(y, 4, f"Documento: {documento}")
        fecha, hora = turno["fecha_hora"]
        self.stdscr.addstr(y+1, 4, f"Turno: {fecha} {hora} - {turno['servicio']} con {turno['profesional']}")
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(y+3, 4, "¿Está seguro que quiere cancelar este turno? (si/no)")
        self.stdscr.attroff(curses.color_pair(4))
        self.stdscr.refresh()
        curses.echo()
        while True:
            self.stdscr.move(y+4, 4)
            self.stdscr.clrtoeol()
            respuesta = self.stdscr.getstr(y+4, 4, 5).decode('utf-8').strip().lower()
            if respuesta.replace(' ', '') == "si":
                curses.noecho()
                return True
            elif respuesta.replace(' ', '') == "no":
                curses.noecho()
                return False
        curses.noecho() 