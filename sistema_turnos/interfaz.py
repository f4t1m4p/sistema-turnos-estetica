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
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  
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
        Muestra los turnos disponibles.
        """
        self.mostrar_titulo("TURNOS DISPONIBLES")
        y = 3
        for i, turno in enumerate(turnos):
            if y < self.altura - 1:
                fecha, hora = turno["fecha_hora"]
                texto = f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}"
                self.stdscr.addstr(y, 2, texto)
                y += 1
        self.stdscr.addstr(self.altura - 2, 2, "Presione ENTER para continuar...")
        self.stdscr.refresh()
        while True:
            tecla = self.stdscr.getch()
            if tecla == 10:  
                break

    def mostrar_mensaje(self, mensaje, tipo="info"):
        """
        Muestra un mensaje al usuario.
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
        self.stdscr.refresh()
        time.sleep(2)

    def pedir_datos(self, prompt):
        """
        Pide datos al usuario.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, prompt)
        self.stdscr.refresh()
        curses.echo()
        datos = self.stdscr.getstr(2, 2).decode('utf-8')
        curses.noecho()
        return datos

    def menu_cliente(self):
        """
        Muestra el menú de cliente.
        """
        opciones = [
            "Ver turnos disponibles",
            "Filtrar turnos",
            "Reservar turno",
            "Cancelar turno",
            "Ver servicios y profesionales",
            "Volver"
        ]
        return self.menu_seleccion(opciones, 3)

    def menu_manicurista(self):
        """
        Muestra el menú de manicurista.
        """
        opciones = [
            "Ver resumen de reservas",
            "Ver nombres de clientes",
            "Volver"
        ]
        return self.menu_seleccion(opciones, 3)

    def mostrar_resumen_reservas(self, reservas):
        """
        Muestra un resumen de las reservas.
        """
        self.mostrar_titulo("RESUMEN DE RESERVAS")
        y = 3
        resumen = {}
        for r in reservas:
            profesional = r["turno"]["profesional"]
            resumen.setdefault(profesional, []).append(r)

        for profesional, lista in resumen.items():
            if y < self.altura - 1:
                self.stdscr.addstr(y, 2, f"\nTurnos de {profesional}:")
                y += 1
                for r in lista:
                    if y < self.altura - 1:
                        fecha, hora = r["turno"]["fecha_hora"]
                        texto = f"- {r['nombre']} el {fecha} a las {hora} para {r['turno']['servicio']}"
                        self.stdscr.addstr(y, 4, texto)
                        y += 1

        self.stdscr.addstr(self.altura - 2, 2, f"Total de reservas: {len(reservas)}")
        self.stdscr.addstr(self.altura - 1, 2, "Presione ENTER para continuar...")
        self.stdscr.refresh()
        while True:
            tecla = self.stdscr.getch()
            if tecla == 10:  
                break 