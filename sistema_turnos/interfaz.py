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
        
        
        self.tamanio_minimo_ancho = 80
        self.tamanio_minimo_altura = 24
        
        if self.ancho < self.tamanio_minimo_ancho or self.altura < self.tamanio_minimo_altura:
            self.mostrar_error_tamanio_pantalla()
            return
        
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  
        curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK)  
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)    
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) 
        curses.curs_set(0)  
        
        self.stdscr.keypad(True) 
        curses.noecho()  
        curses.cbreak()
        
        
        curses.resize_term(self.altura, self.ancho)
    
    def mostrar_error_tamanio_pantalla(self):
        """
        Muestra un mensaje de error cuando la pantalla es muy pequeña.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, "ERROR: Pantalla muy pequeña")
        self.stdscr.addstr(3, 2, f"Tamaño actual: {self.ancho}x{self.altura}")
        self.stdscr.addstr(4, 2, f"Tamaño mínimo requerido: {self.tamanio_minimo_ancho}x{self.tamanio_minimo_altura}")
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
            if self.ancho < self.tamanio_minimo_ancho or self.altura < self.tamanio_minimo_altura:
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

    def mostrar_menu_principal(self):
        """
        Muestra el menú principal.
        """
        self.mostrar_titulo("SISTEMA DE TURNOS")
        opciones = ["Cliente", "Manicurista", "Salir"]
        return self.menu_seleccion(opciones, 3)

    def menu_seleccion(self, opciones, inicio_y):
        """
        Maneja la selección en un menú de forma segura.
        """
        if not self.verificar_tamanio_pantalla():
            return -1
        
        seleccion = 0
        while True:
            self.stdscr.clear()
            
            
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
            
            
            for idx, opcion in enumerate(opciones_vista):
                y = inicio_y + idx
                if y < self.altura - 1:  
                    try:
                        
                        opcion_segura = opcion[:self.ancho - 4] if len(opcion) > self.ancho - 4 else opcion
                        
                        if idx == seleccion_vista:
                            self.stdscr.attron(curses.color_pair(2))
                            self.stdscr.addstr(y, 2, f"> {opcion_segura}")
                            self.stdscr.attroff(curses.color_pair(2))
                        else:
                            self.stdscr.addstr(y, 2, f"  {opcion_segura}")
                    except curses.error:
                       
                        continue

            
            if len(opciones) > max_opciones:
                self.stdscr.attron(curses.color_pair(4))
                if inicio > 0:
                    self.stdscr.addstr(self.altura - 3, 2, "↑ Más opciones arriba")
                if fin < len(opciones):
                    self.stdscr.addstr(self.altura - 3, self.ancho - 20, "Más opciones abajo ↓")
                self.stdscr.attroff(curses.color_pair(4))

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
        Muestra los turnos disponibles con colores de forma segura.
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
        
        if len(turnos) > max_turnos_por_pantalla:
            
            inicio = 0
            while True:
                self.stdscr.clear()
                self.stdscr.attron(curses.color_pair(1))
                x, titulo_seguro = self.centrar_texto("TURNOS DISPONIBLES", 1)
                self.stdscr.addstr(1, x, titulo_seguro)
                self.stdscr.attroff(curses.color_pair(1))
                
                y = 3
                for i in range(inicio, min(inicio + max_turnos_por_pantalla, len(turnos))):
                    if y < self.altura - 3:
                        turno = turnos[i]
                        fecha, hora = turno["fecha_hora"]
                        texto = f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}"
                        
                        texto_seguro = texto[:self.ancho - 4] if len(texto) > self.ancho - 4 else texto
                        self.stdscr.addstr(y, 2, texto_seguro)
                        y += 1
                
                
                self.stdscr.attron(curses.color_pair(4))
                if inicio > 0:
                    self.stdscr.addstr(self.altura - 3, 2, "↑ Anterior")
                if inicio + max_turnos_por_pantalla < len(turnos):
                    self.stdscr.addstr(self.altura - 3, self.ancho - 12, "Siguiente ↓")
                self.stdscr.addstr(self.altura - 2, 2, "ENTER para continuar, ↑↓ para navegar")
                self.stdscr.attroff(curses.color_pair(4))
                
                self.stdscr.refresh()
                tecla = self.stdscr.getch()
                
                if tecla == 10:  
                    break
                elif tecla == curses.KEY_UP and inicio > 0:
                    inicio = max(0, inicio - 1)
                elif tecla == curses.KEY_DOWN and inicio + max_turnos_por_pantalla < len(turnos):
                    inicio = min(len(turnos) - max_turnos_por_pantalla, inicio + 1)
        else:
            
            for i, turno in enumerate(turnos):
                if y < self.altura - 3:
                    fecha, hora = turno["fecha_hora"]
                    texto = f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}"
                    
                    texto_seguro = texto[:self.ancho - 4] if len(texto) > self.ancho - 4 else texto
                    self.stdscr.addstr(y, 2, texto_seguro)
                    y += 1
            
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
        Muestra un mensaje al usuario y espera ENTER para continuar de forma segura.
        """
        if not self.verificar_tamanio_pantalla():
            return
        
        self.stdscr.clear()
        color = {
            "error": 3,
            "info": 4,
            "exito": 2
        }.get(tipo, 4)
        
       
        x, mensaje_seguro = self.centrar_texto(mensaje, self.altura // 2)
        self.stdscr.attron(curses.color_pair(color))
        self.stdscr.addstr(self.altura // 2, x, mensaje_seguro)
        self.stdscr.attroff(curses.color_pair(color))
    
        texto_enter = "Presione ENTER para volver al inicio..."
        if mensaje.strip() != "Gracias por usar el sistema de turnos. ¡Hasta luego!":
            self.stdscr.attron(curses.A_DIM)
            x_enter, texto_enter_seguro = self.centrar_texto(texto_enter, self.altura // 2 + 2)
            self.stdscr.addstr(self.altura // 2 + 2, x_enter, texto_enter_seguro)
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
                if 0 <= ch <= 255:
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
            "Gestionar reservas pendientes",
            "Filtrar turnos",
            "Volver"
        ]
        return self.menu_seleccion(opciones, 4)

    def mostrar_resumen_reservas(self, reservas):
        """
        Muestra un resumen de las reservas en modo navegable y seleccionable.
        """
        self.mostrar_lista_reservas_navegable(reservas)

    def mostrar_lista_reservas_navegable(self, reservas):
        """
        Muestra una lista navegable de reservas. Al seleccionar una, muestra los detalles.
        """
        if not reservas:
            self.stdscr.clear()
            self.stdscr.addstr(2, 2, "No hay reservas para mostrar.")
            self.stdscr.addstr(4, 2, "Presione ENTER para continuar...")
            self.stdscr.refresh()
            while True:
                tecla = self.stdscr.getch()
                if tecla == 10:
                    return
        seleccion = 0
        max_vista = self.altura - 7 
        scroll = 0
        while True:
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(1, (self.ancho - len("RESUMEN DE RESERVAS")) // 2, "RESUMEN DE RESERVAS")
            self.stdscr.attroff(curses.color_pair(1))
            y = 3
            reservas_vista = reservas[scroll:scroll+max_vista]
            for idx, r in enumerate(reservas_vista):
                if y < self.altura - 3:
                    fecha, hora = r["turno"]["fecha_hora"]
                    estado = r.get("estado", "Pendiente")
                    monto = r.get("montoCobrado")
                    texto = f"{scroll+idx+1}. {r['nombre']} - {fecha} {hora} - {r['turno']['servicio']} con {r['turno']['profesional']}"
                    if scroll+idx == seleccion:
                        self.stdscr.attron(curses.color_pair(2))
                        self.stdscr.addstr(y, 2, texto[:self.ancho-5])
                        self.stdscr.attroff(curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y, 2, texto[:self.ancho-5])
                    y += 1
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 3, 2, "↑↓ para navegar, ENTER para ver detalles, ESC para volver"[:self.ancho-5])
            self.stdscr.attroff(curses.color_pair(4))
            self.stdscr.refresh()
            tecla = self.stdscr.getch()
            if tecla == curses.KEY_UP and seleccion > 0:
                seleccion -= 1
                if seleccion < scroll:
                    scroll -= 1
            elif tecla == curses.KEY_DOWN and seleccion < len(reservas) - 1:
                seleccion += 1
                if seleccion >= scroll + max_vista:
                    scroll += 1
            elif tecla == 10:  
                resultado = self.mostrar_detalle_reserva(reservas[seleccion])
                if resultado == 'menu':
                    return 'menu'
            elif tecla == 27: 
                return

    def mostrar_detalle_reserva(self, reserva):
        """
        Muestra una ventana con el detalle completo de la reserva seleccionada.
        """
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len("DETALLE DE RESERVA")) // 2, "DETALLE DE RESERVA")
        self.stdscr.attroff(curses.color_pair(1))
        y = 4
        self.stdscr.addstr(y, 4, f"Cliente: {reserva['nombre']}")
        self.stdscr.addstr(y+1, 4, f"Teléfono: {reserva['telefono']}")
        self.stdscr.addstr(y+2, 4, f"Documento: {reserva['documento']}")
        fecha, hora = reserva["turno"]["fecha_hora"]
        self.stdscr.addstr(y+3, 4, f"Fecha: {fecha} {hora}")
        self.stdscr.addstr(y+4, 4, f"Servicio: {reserva['turno']['servicio']}")
        self.stdscr.addstr(y+5, 4, f"Profesional: {reserva['turno']['profesional']}")
        estado = reserva.get("estado", "Pendiente")
        monto = reserva.get("montoCobrado")
        self.stdscr.addstr(y+6, 4, f"Estado: {estado}")
        if estado == "Atendido" and monto is not None:
            self.stdscr.addstr(y+7, 4, f"Monto cobrado: ${monto:.2f}")
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(self.altura - 2, 2, "Presione ESC para volver, ENTER para ir al menú"[:self.ancho-5])
        self.stdscr.attroff(curses.color_pair(4))
        self.stdscr.refresh()
        while True:
            tecla = self.stdscr.getch()
            if tecla == 27:
                return  
            elif tecla == 10:
                return 'menu'  
    def mostrar_turnos_reservados(self, reservas, dni):
        """
        Muestra los turnos reservados para el documento dado. Permite volver con ESC.
        """
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
                estado = r.get("estado", "Pendiente")
                monto = r.get("montoCobrado")
                texto = f"- {fecha} {hora} - {r['turno']['servicio']} con {r['turno']['profesional']}"
                self.stdscr.addstr(y, 2, texto)
                y += 1
                if y < self.altura - 1:
                    estado_texto = f"  Estado: {estado}"
                    if estado == "Atendido" and monto is not None:
                        estado_texto += f" - Monto cobrado: ${monto:.2f}"
                    elif estado == "No asistió":
                        estado_texto += " - No asistió"
                    if estado == "Atendido":
                        self.stdscr.attron(curses.color_pair(2)) 
                    elif estado == "No asistió":
                        self.stdscr.attron(curses.color_pair(3))  
                    else:
                        self.stdscr.attron(curses.color_pair(4)) 
                    self.stdscr.addstr(y, 4, estado_texto)
                    self.stdscr.attroff(curses.color_pair(2) | curses.color_pair(3) | curses.color_pair(4))
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
        error = False
        while True:
            self.stdscr.move(y+6, 4)
            self.stdscr.clrtoeol()
            if error:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(y+7, 4, "Respuesta inválida. Escriba 'si' o 'no'.")
                self.stdscr.attroff(curses.color_pair(3))
            self.stdscr.refresh()
            respuesta = self.stdscr.getstr(y+6, 4, 5).decode('utf-8').strip().lower()
            if respuesta.replace(' ', '') == "si":
                curses.noecho()
                return True
            elif respuesta.replace(' ', '') == "no":
                curses.noecho()
                return False
            else:
                error = True
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
        error = False
        while True:
            self.stdscr.move(y+4, 4)
            self.stdscr.clrtoeol()
            if error:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(y+5, 4, "Respuesta inválida. Escriba 'si' o 'no'.")
                self.stdscr.attroff(curses.color_pair(3))
            self.stdscr.refresh()
            respuesta = self.stdscr.getstr(y+4, 4, 5).decode('utf-8').strip().lower()
            if respuesta.replace(' ', '') == "si":
                curses.noecho()
                return True
            elif respuesta.replace(' ', '') == "no":
                curses.noecho()
                return False
            else:
                error = True
        curses.noecho()

    def gestionar_reservas_pendientes(self, reservas):
        """
        Permite a la manicurista gestionar sus reservas pendientes.
        Puede marcar como atendida (ingresando monto) o como no asistió.
        """
        from sistema_turnos.turnos import obtener_reservas_pendientes, actualizar_estado_reserva
        from sistema_turnos.datos import guardar_reservas
        
        
        reservas_pendientes = obtener_reservas_pendientes(reservas)
        
        if not reservas_pendientes:
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(1, (self.ancho - len("GESTIONAR RESERVAS PENDIENTES")) // 2, "GESTIONAR RESERVAS PENDIENTES")
            self.stdscr.attroff(curses.color_pair(1))
            self.stdscr.attron(curses.color_pair(3))
            self.stdscr.addstr(3, 2, "No hay reservas pendientes.")
            self.stdscr.attroff(curses.color_pair(3))
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 2, 2, "Presione ENTER para continuar...")
            self.stdscr.attroff(curses.color_pair(4))
            self.stdscr.refresh()
            while True:
                tecla = self.stdscr.getch()
                if tecla == 10:
                    break
            return
        

        seleccion = 0
        while True:
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(1, (self.ancho - len("RESERVAS PENDIENTES")) // 2, "RESERVAS PENDIENTES")
            self.stdscr.attroff(curses.color_pair(1))
            
            y = 3
            for i, reserva in enumerate(reservas_pendientes):
                if y < self.altura - 4:
                    fecha, hora = reserva["turno"]["fecha_hora"]
                    texto = f"{i+1}. {reserva['nombre']} - {fecha} {hora} - {reserva['turno']['servicio']} con {reserva['turno']['profesional']}"
                    
                    if i == seleccion:
                        self.stdscr.attron(curses.color_pair(2))
                        self.stdscr.addstr(y, 2, texto)
                        self.stdscr.attroff(curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y, 2, texto)
                    y += 1
            
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 3, 2, "↑↓ para navegar, ENTER para seleccionar, ESC para volver")
            self.stdscr.attroff(curses.color_pair(4))
            self.stdscr.refresh()
            
            tecla = self.stdscr.getch()
            if tecla == curses.KEY_UP and seleccion > 0:
                seleccion -= 1
            elif tecla == curses.KEY_DOWN and seleccion < len(reservas_pendientes) - 1:
                seleccion += 1
            elif tecla == 10: 
                
                self.mostrar_opciones_reserva(reservas_pendientes[seleccion], reservas)
                break
            elif tecla == 27:  
                break
    
    def mostrar_opciones_reserva(self, reserva, reservas):
        """
        Muestra las opciones para una reserva específica (marcar como atendida o no asistió).
        Ahora se escribe 'atendida' o 'no asistio' en vez de elegir con números.
        """
        from sistema_turnos.turnos import actualizar_estado_reserva
        from sistema_turnos.datos import guardar_reservas
        import unicodedata
        
        def normalizar(texto):
            return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower().strip()
        
        while True:
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(1, (self.ancho - len("GESTIONAR RESERVA")) // 2, "GESTIONAR RESERVA")
            self.stdscr.attroff(curses.color_pair(1))
            
            y = 3
            x_info = 2
            fecha, hora = reserva["turno"]["fecha_hora"]
            self.stdscr.addstr(y, x_info, f"Cliente: {reserva['nombre']}")
            self.stdscr.addstr(y+1, x_info, f"Fecha: {fecha} {hora}")
            self.stdscr.addstr(y+2, x_info, f"Servicio: {reserva['turno']['servicio']}")
            self.stdscr.addstr(y+3, x_info, f"Profesional: {reserva['turno']['profesional']}")
            self.stdscr.addstr(y+4, x_info, f"Documento: {reserva['documento']}")
            

            x_opciones = self.ancho // 2 + 4
            y_op = y
            self.stdscr.attron(curses.color_pair(2))
            self.stdscr.addstr(y_op, x_opciones, "Escriba: atendida  o  no asistio")
            self.stdscr.attroff(curses.color_pair(2))
            

            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 2, 2, "ENTER para confirmar, ESC para volver"[:self.ancho-5])
            self.stdscr.attroff(curses.color_pair(4))
            self.stdscr.refresh()
            
            curses.echo()
            buffer = b""
            while True:
                ch = self.stdscr.getch(y_op + 3, x_opciones + len(buffer))
                if ch == 27:  
                    curses.noecho()
                    return
                elif ch in (10, 13): 
                    break
                elif ch in (8, 127):  
                    if buffer:
                        buffer = buffer[:-1]
                        self.stdscr.move(y_op + 3, x_opciones + len(buffer))
                        self.stdscr.delch()
                else:
                    if 0 <= ch <= 255:
                        buffer += bytes([ch])
                        self.stdscr.addch(y_op + 3, x_opciones + len(buffer) - 1, ch)
            curses.noecho()
            entrada = buffer.decode('utf-8').strip()
            if entrada == '':
                continue
            accion = normalizar(entrada)
            if accion == 'atendida':
                self.marcar_como_atendida(reserva, reservas)
                break
            elif accion == 'no asistio':
                # Aplicar directamente el cambio sin confirmación adicional
                if actualizar_estado_reserva(reservas, reserva["documento"], "No asistió"):
                    guardar_reservas(reservas)
                    self.mostrar_mensaje("Reserva marcada como 'No asistió'", "exito")
                else:
                    self.mostrar_mensaje("Error al actualizar la reserva", "error")
                break
            elif entrada == '':
                continue
            else:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(self.altura - 3, 2, "Acción inválida. Escriba 'atendida' o 'no asistio'."[:self.ancho-5])
                self.stdscr.attroff(curses.color_pair(3))
                self.stdscr.refresh()
                curses.napms(1500)
    
    def marcar_como_atendida(self, reserva, reservas):
        """
        Permite marcar una reserva como atendida e ingresar el monto cobrado.
        """
        from sistema_turnos.turnos import actualizar_estado_reserva
        from sistema_turnos.datos import guardar_reservas
        
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len("MARCAR COMO ATENDIDA")) // 2, "MARCAR COMO ATENDIDA")
        self.stdscr.attroff(curses.color_pair(1))
        
        fecha, hora = reserva["turno"]["fecha_hora"]
        y = 3
        self.stdscr.addstr(y, 2, f"Cliente: {reserva['nombre']}")
        self.stdscr.addstr(y+1, 2, f"Fecha: {fecha} {hora}")
        self.stdscr.addstr(y+2, 2, f"Servicio: {reserva['turno']['servicio']}")
        
        y += 4
        self.stdscr.addstr(y, 2, "Ingrese el monto cobrado:")
        self.stdscr.refresh()
        
        curses.echo()
        while True:
            self.stdscr.move(y+1, 2)
            self.stdscr.clrtoeol()
            monto_str = self.stdscr.getstr(y+1, 2, 20).decode('utf-8').strip()
            
            try:
                monto = float(monto_str)
                if monto <= 0:
                    raise ValueError("El monto debe ser mayor a 0")
                break
            except ValueError:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(y+2, 2, "Error: Ingrese un monto válido (número mayor a 0)")
                self.stdscr.attroff(curses.color_pair(3))
                self.stdscr.refresh()
                curses.napms(2000)
                self.stdscr.move(y+2, 0)
                self.stdscr.clrtoeol()
        
        curses.noecho()
        
        
        if actualizar_estado_reserva(reservas, reserva["documento"], "Atendido", monto):
            guardar_reservas(reservas)
            self.mostrar_mensaje(f"Reserva marcada como atendida. Monto: ${monto:.2f}", "exito")
        else:
            self.mostrar_mensaje("Error al actualizar la reserva", "error") 