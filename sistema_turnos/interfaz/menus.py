"""
Módulo de menús para el sistema de turnos.
Contiene las funciones para mostrar y manejar menús de selección.
"""

import curses

class MenusInterfaz:
    """
    Clase que maneja los menús de selección del sistema.
    """
    
    def __init__(self, stdscr, altura, ancho):
        self.stdscr = stdscr
        self.altura = altura
        self.ancho = ancho
    
    def mostrar_menu_principal(self):
        """
        Muestra el menú principal.
        """
        opciones = ["Cliente", "Manicurista", "Salir"]
        return self.menu_seleccion(opciones, 3)
    
    def menu_cliente(self):
        """
        Muestra el menú de cliente.
        """
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
        opciones = [
            "Ver resumen de reservas",
            "Gestionar reservas pendientes",
            "Filtrar reservas por estado",
            "Volver"
        ]
        return self.menu_seleccion(opciones, 3)
    
    def menu_seleccion(self, opciones, inicio_y):
        """
        Maneja la selección en un menú de forma segura.
        """
        seleccion = 0
        while True:
            self.stdscr.clear()
            
            # Calcular cuántas opciones caben en pantalla
            max_opciones = self.altura - inicio_y - 2
            if len(opciones) > max_opciones:
                # Implementar scroll para muchas opciones
                inicio = max(0, seleccion - max_opciones // 2)
                fin = min(len(opciones), inicio + max_opciones)
                opciones_vista = opciones[inicio:fin]
                seleccion_vista = seleccion - inicio
            else:
                opciones_vista = opciones
                seleccion_vista = seleccion
            
            # Mostrar opciones
            for idx, opcion in enumerate(opciones_vista):
                y = inicio_y + idx
                if y < self.altura - 1:
                    try:
                        # Truncar opción si es muy larga
                        opcion_segura = opcion[:self.ancho - 4] if len(opcion) > self.ancho - 4 else opcion
                        
                        if idx == seleccion_vista:
                            self.stdscr.attron(curses.color_pair(2))
                            self.stdscr.addstr(y, 2, f"> {opcion_segura}")
                            self.stdscr.attroff(curses.color_pair(2))
                        else:
                            self.stdscr.addstr(y, 2, f"  {opcion_segura}")
                    except curses.error:
                        continue
            
            # Mostrar indicadores de scroll
            if len(opciones) > max_opciones:
                self.stdscr.attron(curses.color_pair(4))
                if inicio > 0:
                    self.stdscr.addstr(self.altura - 3, 2, "↑ Más opciones arriba")
                if fin < len(opciones):
                    self.stdscr.addstr(self.altura - 3, self.ancho - 20, "Más opciones abajo ↓")
                self.stdscr.attroff(curses.color_pair(4))
            
            self.stdscr.refresh()
            tecla = self.stdscr.getch()
            
            # Manejar navegación
            if tecla == curses.KEY_UP:
                seleccion = max(0, seleccion - 1)
            elif tecla == curses.KEY_DOWN:
                seleccion = min(len(opciones) - 1, seleccion + 1)
            elif tecla == 10:  # Enter
                return seleccion
            elif tecla == 27:  # ESC
                return -1
    
    def pedir_filtro_servicio(self, opciones_servicio):
        """
        Pide al usuario que ingrese un filtro de servicio.
        """
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(1, 2, "Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ")
            self.stdscr.addstr(self.altura - 2, 2, "ESC para volver")
            if 'error_servicio' in locals() and error_servicio:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(2, 2, "Servicio inválido. Opciones: Kapping, Semi, Soft Gel.")
                self.stdscr.attroff(curses.color_pair(3))
            self.stdscr.move(3, 2)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            curses.echo()
            servicio = self._input_curses_utf8(3, 2, 50)
            curses.noecho()
            
            if servicio is None:
                return None
            
            servicio = servicio.lower()
            if servicio == "":
                return None
            
            if not servicio.replace(" ", "").isalpha() or servicio not in opciones_servicio:
                error_servicio = True
                continue
            
            return servicio
    
    def pedir_filtro_profesional(self, opciones_profesional):
        """
        Pide al usuario que ingrese un filtro de profesional.
        """
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(1, 2, "Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ")
            self.stdscr.addstr(self.altura - 2, 2, "ESC para volver")
            if 'error_prof' in locals() and error_prof:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(2, 2, "Profesional inválido. Opciones: Gisela, Marisol, Valentina.")
                self.stdscr.attroff(curses.color_pair(3))
            self.stdscr.move(3, 2)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            curses.echo()
            profesional = self._input_curses_utf8(3, 2, 50)
            curses.noecho()
            
            if profesional is None:
                return None
            
            profesional = profesional.lower()
            if profesional == "":
                return None
            
            if not profesional.replace(" ", "").isalpha() or profesional not in opciones_profesional:
                error_prof = True
                continue
            
            return profesional
    
    def pedir_filtro_estado(self, opciones_estado):
        """
        Pide al usuario que ingrese un filtro de estado.
        """
        # Unificar opciones a mayúscula inicial
        opciones_estado = [op.capitalize() if op != "No asistió" else "No asistió" for op in opciones_estado]
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(1, 2, "Filtrar por estado (Pendiente, Atendida, No asistió o ENTER): ")
            self.stdscr.addstr(self.altura - 2, 2, "ESC para volver")
            if 'error_estado' in locals() and error_estado:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(2, 2, "Estado inválido. Opciones: Pendiente, Atendida, No asistió.")
                self.stdscr.attroff(curses.color_pair(3))
            self.stdscr.move(3, 2)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            curses.echo()
            estado = self._input_curses_utf8(3, 2, 50)
            curses.noecho()
            if estado is None:
                return None
            estado = estado.strip().capitalize() if estado.strip().lower() != "no asistió" else "No asistió"
            if estado == "":
                return None
            if not estado.replace(" ", "").isalpha() or estado not in opciones_estado:
                error_estado = True
                continue
            return estado
    
    def _input_curses_utf8(self, y, x, maxlen=50):
        """
        Función auxiliar para entrada de texto con curses, soportando caracteres UTF-8 (como ñ y acentos).
        """
        try:
            self.stdscr.move(y, x)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            entrada = ""
            while True:
                tecla = self.stdscr.get_wch()  # get_wch soporta unicode
                if isinstance(tecla, str):
                    if tecla == '\x1b':  # ESC
                        return None
                    elif tecla == '\n':  # Enter
                        return entrada
                    elif tecla in ('\b', '\x7f', '\x08'):  # Backspace
                        if entrada:
                            entrada = entrada[:-1]
                            self.stdscr.move(y, x + len(entrada))
                            self.stdscr.delch()
                    elif len(entrada) < maxlen and (tecla.isprintable()):
                        entrada += tecla
                        self.stdscr.addstr(y, x + len(entrada) - 1, tecla)
                elif isinstance(tecla, int):
                    if tecla == 27:  # ESC
                        return None
                    elif tecla == 10:  # Enter
                        return entrada
                    elif tecla in (127, 8):  # Backspace
                        if entrada:
                            entrada = entrada[:-1]
                            self.stdscr.move(y, x + len(entrada))
                            self.stdscr.delch()
                self.stdscr.refresh()
        except Exception as e:
            return None 