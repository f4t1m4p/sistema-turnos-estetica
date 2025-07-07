"""
Módulo de pantalla para el sistema de turnos.
Contiene funciones para limpieza, colores y helpers visuales.
"""

import curses
import time

class PantallaInterfaz:
    """
    Clase que maneja la presentación visual del sistema.
    """
    
    def __init__(self, stdscr, altura, ancho):
        self.stdscr = stdscr
        self.altura = altura
        self.ancho = ancho
    
    def mostrar_error_tamanio_pantalla(self):
        """
        Muestra un mensaje de error cuando la pantalla es muy pequeña.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, "ERROR: Pantalla muy pequeña")
        self.stdscr.addstr(3, 2, f"Tamaño actual: {self.ancho}x{self.altura}")
        self.stdscr.addstr(4, 2, f"Tamaño mínimo requerido: 80x24")
        self.stdscr.addstr(6, 2, "Por favor:")
        self.stdscr.addstr(7, 2, "1. Aumenta el tamaño de tu terminal")
        self.stdscr.addstr(8, 2, "2. O usa una fuente más pequeña")
        self.stdscr.addstr(9, 2, "3. O maximiza la ventana")
        self.stdscr.addstr(11, 2, "Presiona cualquier tecla para salir...")
        self.stdscr.refresh()
        self.stdscr.getch()
    
    def verificar_tamanio_pantalla(self):
        """
        Verifica si el tamaño de pantalla sigue siendo válido.
        """
        nueva_altura, nuevo_ancho = self.stdscr.getmaxyx()
        if nuevo_ancho != self.ancho or nueva_altura != self.altura:
            self.altura, self.ancho = nueva_altura, nuevo_ancho
            if self.ancho < 80 or self.altura < 24:
                self.mostrar_error_tamanio_pantalla()
                return False
        return True
    
    def centrar_texto(self, texto, y, max_ancho=None):
        """
        Centra un texto en la pantalla de forma segura.
        """
        if max_ancho is None:
            max_ancho = self.ancho - 4
        
        texto_truncado = texto[:max_ancho] if len(texto) > max_ancho else texto
        x = max(2, (self.ancho - len(texto_truncado)) // 2)
        return x, texto_truncado
    
    def mostrar_titulo(self, titulo):
        """
        Muestra un título en la pantalla de forma segura.
        """
        if not self.verificar_tamanio_pantalla():
            return
        
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        x, texto_seguro = self.centrar_texto(titulo, 1)
        self.stdscr.addstr(1, x, texto_seguro)
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.refresh()
    
    def mostrar_mensaje(self, mensaje, tipo="info"):
        """
        Muestra un mensaje en la pantalla con el tipo especificado.
        """
        if not self.verificar_tamanio_pantalla():
            return
        
        self.stdscr.clear()
        
        # Seleccionar color según el tipo
        if tipo == "error":
            self.stdscr.attron(curses.color_pair(3))  # Rojo
        elif tipo == "exito":
            self.stdscr.attron(curses.color_pair(1))  # Cyan
        elif tipo == "advertencia":
            self.stdscr.attron(curses.color_pair(4))  # Amarillo
        else:
            self.stdscr.attron(curses.color_pair(2))  # Magenta
        
        # Centrar y mostrar mensaje
        x, texto_seguro = self.centrar_texto(mensaje, self.altura // 2)
        self.stdscr.addstr(self.altura // 2, x, texto_seguro)
        
        self.stdscr.attroff(curses.color_pair(1))
        self.stdscr.attroff(curses.color_pair(2))
        self.stdscr.attroff(curses.color_pair(3))
        self.stdscr.attroff(curses.color_pair(4))
        
        # Mostrar instrucciones
        self.stdscr.addstr(self.altura - 2, 2, "Presiona cualquier tecla para continuar...")
        self.stdscr.refresh()
        self.stdscr.getch()
    
    def mostrar_turnos(self, turnos):
        """
        Muestra los turnos disponibles con un cursor visual para navegación (sin selección).
        """
        if not self.verificar_tamanio_pantalla():
            return
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        x, titulo_seguro = self.centrar_texto("TURNOS DISPONIBLES", 1)
        self.stdscr.addstr(1, x, titulo_seguro)
        self.stdscr.attroff(curses.color_pair(1))
        y = 3
        max_turnos_por_pantalla = self.altura - 5
        seleccion = 0
        scroll = 0
        while True:
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            x, titulo_seguro = self.centrar_texto("TURNOS DISPONIBLES", 1)
            self.stdscr.addstr(1, x, titulo_seguro)
            self.stdscr.attroff(curses.color_pair(1))
            y = 3
            turnos_vista = turnos[scroll:scroll+max_turnos_por_pantalla]
            for idx, turno in enumerate(turnos_vista):
                if y < self.altura - 3:
                    fecha, hora = turno["fecha_hora"]
                    texto = f"{scroll+idx+1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}"
                    texto_seguro = texto[:self.ancho - 4] if len(texto) > self.ancho - 4 else texto
                    if scroll+idx == seleccion:
                        self.stdscr.attron(curses.color_pair(2))
                        self.stdscr.addstr(y, 2, texto_seguro)
                        self.stdscr.attroff(curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y, 2, texto_seguro)
                    y += 1
            self.stdscr.addstr(self.altura - 2, 2, "↑↓ para navegar, ESC o ENTER para salir")
            self.stdscr.refresh()
            tecla = self.stdscr.getch()
            if tecla == curses.KEY_UP and seleccion > 0:
                seleccion -= 1
                if seleccion < scroll:
                    scroll -= 1
            elif tecla == curses.KEY_DOWN and seleccion < len(turnos) - 1:
                seleccion += 1
                if seleccion >= scroll + max_turnos_por_pantalla:
                    scroll += 1
            elif tecla == 27 or tecla == 10:
                break
    
    def limpiar_pantalla(self):
        """
        Limpia la pantalla completamente.
        """
        self.stdscr.clear()
        self.stdscr.refresh()
    
    def mostrar_loading(self, mensaje="Cargando..."):
        """
        Muestra un mensaje de carga.
        """
        self.stdscr.clear()
        x, texto_seguro = self.centrar_texto(mensaje, self.altura // 2)
        self.stdscr.addstr(self.altura // 2, x, texto_seguro)
        self.stdscr.refresh()
        time.sleep(0.5) 