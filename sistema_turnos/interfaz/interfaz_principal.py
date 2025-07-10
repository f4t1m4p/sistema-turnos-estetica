"""
Interfaz de usuario del sistema de turnos.
Clase principal que coordina los módulos de interfaz.
"""

import curses
from sistema_turnos.interfaz.menus import MenusInterfaz
from sistema_turnos.interfaz.pantalla import PantallaInterfaz

class InterfazTurnos:
    """
    Clase principal que maneja la interfaz de usuario.
    Coordina los módulos de menús y pantalla.
    """
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.altura, self.ancho = stdscr.getmaxyx()
        
        # Configuración de tamaño mínimo
        self.tamanio_minimo_ancho = 80
        self.tamanio_minimo_altura = 24
        
        if self.ancho < self.tamanio_minimo_ancho or self.altura < self.tamanio_minimo_altura:
            self.mostrar_error_tamanio_pantalla()
            return
        
        # Configurar curses solo si el tamaño es válido
        try:
            curses.start_color()
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)   # Títulos
            curses.init_pair(2, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Selección
            curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # Errores
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Advertencias
            curses.curs_set(0)  # Ocultar cursor
            self.stdscr.keypad(True)  # Habilitar teclas especiales
            curses.noecho()  # No mostrar teclas presionadas
            curses.cbreak()  # Modo cbreak
            
            # Redimensionar terminal
            curses.resize_term(self.altura, self.ancho)
            
            # Inicializar módulos de interfaz
            self.menus = MenusInterfaz(stdscr, self.altura, self.ancho)
            self.pantalla = PantallaInterfaz(stdscr, self.altura, self.ancho)
        except:
            pass
        

    
    def mostrar_error_tamanio_pantalla(self):
        """
        Muestra un mensaje de error cuando la pantalla es muy pequeña.
        """
        try:
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
        except:
            pass
    
    def mostrar_mensaje(self, mensaje, tipo="info"):
        """
        Muestra un mensaje al usuario.
        """
        self.pantalla.mostrar_mensaje(mensaje, tipo)
    
    def mostrar_turnos(self, turnos):
        """
        Muestra los turnos disponibles.
        """
        self.pantalla.mostrar_turnos(turnos)
    
    def mostrar_menu_principal(self):
        """
        Muestra el menú principal.
        """
        return self.menus.mostrar_menu_principal()
    
    def menu_cliente(self):
        """
        Muestra el menú de cliente.
        """
        return self.menus.menu_cliente()
    
    def menu_manicurista(self):
        """
        Muestra el menú de manicurista.
        """
        return self.menus.menu_manicurista()
    
    def pedir_filtro_servicio(self, opciones_servicio):
        """
        Pide al usuario que ingrese un filtro de servicio.
        """
        return self.menus.pedir_filtro_servicio(opciones_servicio)
    
    def pedir_filtro_profesional(self, opciones_profesional):
        """
        Pide al usuario que ingrese un filtro de profesional.
        """
        return self.menus.pedir_filtro_profesional(opciones_profesional)
    
    def pedir_filtro_estado(self, opciones_estado):
        """
        Pide al usuario que ingrese un filtro de estado.
        """
        return self.menus.pedir_filtro_estado(opciones_estado)
    
    def mostrar_resumen_reservas(self, reservas):
        """
        Muestra un resumen de las reservas agrupadas por profesional y permite seleccionar una.
        Devuelve la reserva seleccionada o None si cancela.
        """
        if not reservas:
            self.mostrar_mensaje("No hay reservas para mostrar.", "info")
            return None
        
        # Agrupar reservas por profesional usando setdefault()
        profesionales = {}
        for r in reservas:
            profesional = r["turno"]["profesional"].capitalize()
            profesionales.setdefault(profesional, []).append(r)
        
        # Usar conjunto para obtener servicios únicos sin repeticiones
        servicios_unicos = set()
        for r in reservas:
            servicios_unicos.add(r["turno"]["servicio"])
        
        seleccion = 0
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(1, (self.ancho - len("RESUMEN DE RESERVAS")) // 2, "RESUMEN DE RESERVAS")
            y = 3
            max_lineas = self.altura - 5
            visibles = []  # Lista de reservas en el orden visual
            
            # Mostrar estadísticas usando conjuntos
            self.stdscr.attron(curses.color_pair(2))
            self.stdscr.addstr(y, 2, f"Servicios disponibles: {', '.join(sorted(servicios_unicos))}")
            self.stdscr.attroff(curses.color_pair(2))
            y += 2
            
            # Construir la lista de reservas visibles y pintar usando .items()
            for profesional, reservas_prof in profesionales.items():
                if y >= max_lineas + 3:
                    break
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, 2, f"{profesional} ({len(reservas_prof)} reservas)")
                self.stdscr.attroff(curses.color_pair(1))
                y += 1
                for r in reservas_prof:
                    if y >= max_lineas + 3:
                        break
                    # Usar tupla para fecha y hora
                    fecha, hora = r["turno"]["fecha_hora"]
                    estado = r.get("estado", "Pendiente")
                    monto = r.get("montoCobrado")
                    texto = f"- {fecha} {hora} - {r['turno']['servicio']} - {r['nombre']} ({estado})"
                    if monto is not None:
                        texto += f" - ${monto:.2f}"
                    visibles.append(r)
                    idx_visual = len(visibles) - 1
                    if idx_visual == seleccion:
                        self.stdscr.attron(curses.color_pair(2))
                        self.stdscr.addstr(y, 2, texto[:self.ancho-4])
                        self.stdscr.attroff(curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y, 2, texto[:self.ancho-4])
                    y += 1
                if y < max_lineas + 3:
                    y += 1  # Espacio entre profesionales
            
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 3, 2, f"↑↓ para navegar ({seleccion+1}/{len(visibles)}), ENTER para ver detalles, ESC para volver")
            self.stdscr.attroff(curses.color_pair(4))
            self.stdscr.refresh()
            
            tecla = self.stdscr.getch()
            if tecla == curses.KEY_UP and seleccion > 0:
                seleccion -= 1
            elif tecla == curses.KEY_DOWN and seleccion < len(visibles) - 1:
                seleccion += 1
            elif tecla == 10 and visibles:
                return visibles[seleccion]
            elif tecla == 27:
                return None

    def mostrar_lista_reservas_navegable(self, reservas):
        """
        Muestra una lista navegable de reservas y permite seleccionar una.
        Devuelve la reserva seleccionada o None si cancela.
        """
        if not reservas:
            self.mostrar_mensaje("No hay reservas para mostrar.", "info")
            return None
        seleccion = 0
        scroll = 0
        max_vista = self.altura - 7
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(1, (self.ancho - len("RESERVAS")) // 2, "RESERVAS")
            y = 3
            reservas_vista = reservas[scroll:scroll+max_vista]
            for idx, r in enumerate(reservas_vista):
                fecha, hora = r["turno"]["fecha_hora"]
                estado = r.get("estado", "Pendiente")
                texto = f"{scroll+idx+1}. {fecha} {hora} - {r['turno']['servicio']} con {r['turno']['profesional']} ({estado})"
                if scroll+idx == seleccion:
                    self.stdscr.attron(curses.color_pair(2))
                    self.stdscr.addstr(y, 2, texto[:self.ancho-4])
                    self.stdscr.attroff(curses.color_pair(2))
                else:
                    self.stdscr.addstr(y, 2, texto[:self.ancho-4])
                y += 1
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 3, 2, "↑↓ para navegar, ENTER para elegir, ESC para cancelar")
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
                return reservas[seleccion]
            elif tecla == 27:
                return None

    def mostrar_opciones_reserva(self, reserva, reservas):
        """
        Permite a la manicurista gestionar una reserva de forma intuitiva.
        Muestra datos del cliente a la izquierda y opciones de estado a la derecha.
        """
        while True:
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(1, (self.ancho - len("GESTIONAR RESERVA")) // 2, "GESTIONAR RESERVA")
            self.stdscr.attroff(curses.color_pair(1))
            
            # Datos del cliente a la izquierda
            x_izq = 2
            y = 4
            fecha, hora = reserva["turno"]["fecha_hora"]
            self.stdscr.addstr(y, x_izq, f"Turno: {fecha} {hora}")
            self.stdscr.addstr(y+1, x_izq, f"Servicio: {reserva['turno']['servicio']}")
            self.stdscr.addstr(y+2, x_izq, f"Profesional: {reserva['turno']['profesional']}")
            self.stdscr.addstr(y+3, x_izq, f"Cliente: {reserva['nombre']}")
            self.stdscr.addstr(y+4, x_izq, f"Teléfono: {reserva['telefono']}")
            self.stdscr.addstr(y+5, x_izq, f"DNI: {reserva['documento']}")
            self.stdscr.addstr(y+6, x_izq, f"Estado actual: {reserva.get('estado', 'Pendiente')}")
            
            # Opciones de estado a la derecha
            x_der = int(self.ancho * 0.6)
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(y, x_der, "CAMBIAR ESTADO:")
            self.stdscr.attroff(curses.color_pair(1))
            self.stdscr.addstr(y+1, x_der, "Escriba 'atendida' o 'no asistió'")
            self.stdscr.addstr(y+2, x_der, "Si es 'atendida', se pedirá el monto")
            self.stdscr.addstr(y+3, x_der, "Presione ENTER para confirmar")
            self.stdscr.addstr(y+4, x_der, "ESC para cancelar")
            
            # Input de estado
            self.stdscr.addstr(y+6, x_der, "Estado: ")
            self.stdscr.refresh()
            curses.echo()
            estado = self.menus._input_curses_utf8(y+6, x_der+7, 20)
            curses.noecho()
            
            if estado is None:
                return
            
            estado = estado.strip().lower()
            if estado not in ["atendida", "no asistió"]:
                self.mostrar_mensaje("Estado inválido. Debe ser 'atendida' o 'no asistió'.", "error")
                continue
            
            # Si es atendida, pedir monto
            monto = None
            if estado == "atendida":
                self.stdscr.addstr(y+8, x_der, "Monto cobrado: $")
                self.stdscr.refresh()
                curses.echo()
                monto_str = self.menus._input_curses_utf8(y+8, x_der+16, 15)
                curses.noecho()
                
                if monto_str is None:
                    return
                
                try:
                    monto = float(monto_str.replace(",", "."))
                    if monto < 0:
                        raise ValueError
                except ValueError:
                    self.mostrar_mensaje("Monto inválido. Ingrese un número positivo.", "error")
                    continue
            
            # Mostrar confirmación
            self.stdscr.clear()
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(1, (self.ancho - len("CONFIRMAR CAMBIO")) // 2, "CONFIRMAR CAMBIO")
            self.stdscr.attroff(curses.color_pair(1))
            y_conf = 4
            self.stdscr.addstr(y_conf, 4, f"Cliente: {reserva['nombre']} - DNI: {reserva['documento']}")
            self.stdscr.addstr(y_conf+1, 4, f"Turno: {fecha} {hora} - {reserva['turno']['servicio']}")
            self.stdscr.addstr(y_conf+2, 4, f"Nuevo estado: {estado.capitalize()}")
            if monto is not None:
                self.stdscr.addstr(y_conf+3, 4, f"Monto cobrado: ${monto:.2f}")
            
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(y_conf+5, 4, "¿Confirmar cambio? (si/no)")
            self.stdscr.attroff(curses.color_pair(4))
            self.stdscr.refresh()
            
            curses.echo()
            error = False
            while True:
                self.stdscr.move(y_conf+6, 4)
                self.stdscr.clrtoeol()
                if error:
                    self.stdscr.attron(curses.color_pair(3))
                    self.stdscr.addstr(y_conf+7, 4, "Respuesta inválida. Escriba 'si' o 'no'.")
                    self.stdscr.attroff(curses.color_pair(3))
                self.stdscr.refresh()
                respuesta = self.menus._input_curses_utf8(y_conf+6, 4, 5)
                if respuesta is None:
                    curses.noecho()
                    return
                respuesta = respuesta.strip().lower()
                if respuesta.replace(' ', '') == "si":
                    curses.noecho()
                    # Aplicar cambios
                    if estado == "atendida":
                        from sistema_turnos.logica.atencion import marcar_como_atendida, cambiar_monto_cobrado
                        resultado = marcar_como_atendida(reserva, reservas)
                        if resultado["exito"] and monto is not None:
                            resultado_monto = cambiar_monto_cobrado(reserva, monto, reservas)
                            if resultado_monto["exito"]:
                                self.mostrar_mensaje("Reserva marcada como atendida y monto registrado.", "exito")
                            else:
                                self.mostrar_mensaje(resultado_monto["error"], "error")
                        elif resultado["exito"]:
                            self.mostrar_mensaje("Reserva marcada como atendida.", "exito")
                        else:
                            self.mostrar_mensaje(resultado["error"], "error")
                    else:
                        from sistema_turnos.logica.atencion import marcar_como_no_asistio
                        resultado = marcar_como_no_asistio(reserva, reservas)
                        if resultado["exito"]:
                            self.mostrar_mensaje("Reserva marcada como no asistió.", "exito")
                        else:
                            self.mostrar_mensaje(resultado["error"], "error")
                    return
                elif respuesta.replace(' ', '') == "no":
                    curses.noecho()
                    return
                else:
                    error = True

    def confirmar_reserva(self, turno, nombre, telefono, documento):
        """
        Confirma una reserva con el usuario mostrando los datos y pidiendo confirmación.
        """
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len("CONFIRMAR RESERVA")) // 2, "CONFIRMAR RESERVA")
        self.stdscr.attroff(curses.color_pair(1))
        y = 4
        self.stdscr.addstr(y, 4, f"Nombre: {nombre}")
        self.stdscr.addstr(y+1, 4, f"Teléfono: {telefono}")
        self.stdscr.addstr(y+2, 4, f"Documento: {documento}")
        fecha, hora = turno["fecha_hora"]
        self.stdscr.addstr(y+3, 4, f"Turno: {fecha} {hora} - {turno['servicio']} con {turno['profesional']}")
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(y+5, 4, "¿Confirmar reserva? (si/no)")
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
            respuesta = self.menus._input_curses_utf8(y+6, 4, 5)
            if respuesta is None:
                curses.noecho()
                return False
            respuesta = respuesta.strip().lower()
            if respuesta.replace(' ', '') == "si":
                curses.noecho()
                return True
            elif respuesta.replace(' ', '') == "no":
                curses.noecho()
                return False
            else:
                error = True
    
    def mostrar_turnos_reservados(self, reservas, dni):
        """
        Muestra los turnos reservados para el documento dado. Permite seleccionar uno con el cursor y volver con ESC.
        Devuelve la reserva seleccionada o None si cancela.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, (self.ancho - len("MIS TURNOS RESERVADOS")) // 2, "MIS TURNOS RESERVADOS")
        y = 4
        encontrados = False
        if not reservas:
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
        seleccion = 0
        scroll = 0
        max_vista = self.altura - 7
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(1, (self.ancho - len("MIS TURNOS RESERVADOS")) // 2, "MIS TURNOS RESERVADOS")
            y = 4
            reservas_vista = reservas[scroll:scroll+max_vista]
            for idx, r in enumerate(reservas_vista):
                fecha, hora = r["turno"]["fecha_hora"]
                estado = r.get("estado", "Pendiente")
                monto = r.get("montoCobrado")
                texto = f"{scroll+idx+1}. {fecha} {hora} - {r['turno']['servicio']} con {r['turno']['profesional']}"
                if scroll+idx == seleccion:
                    self.stdscr.attron(curses.color_pair(2))
                    self.stdscr.addstr(y, 2, texto)
                    self.stdscr.attroff(curses.color_pair(2))
                else:
                    self.stdscr.addstr(y, 2, texto)
                y += 1
                if y < self.altura - 1:
                    estado_texto = f"  Estado: {estado}"
                    if estado == "Atendida" and monto is not None:
                        estado_texto += f" - Monto cobrado: ${monto:.2f}"
                    elif estado == "No asistió":
                        estado_texto += " - No asistió"
                    if estado == "Atendida":
                        self.stdscr.attron(curses.color_pair(2)) 
                    elif estado == "No asistió":
                        self.stdscr.attron(curses.color_pair(3))  
                    else:
                        self.stdscr.attron(curses.color_pair(4)) 
                    self.stdscr.addstr(y, 4, estado_texto)
                    self.stdscr.attroff(curses.color_pair(2) | curses.color_pair(3) | curses.color_pair(4))
                    y += 1
            self.stdscr.attron(curses.color_pair(4))
            self.stdscr.addstr(self.altura - 2, 2, "↑↓ para navegar, ENTER para seleccionar, ESC para volver")
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
                return reservas[seleccion]
            elif tecla == 27:
                return None

    def pedir_dni_cliente(self):
        """
        Pide el DNI del cliente.
        """
        self.stdscr.clear()
        self.stdscr.addstr(1, 2, "Ingrese su DNI: ")
        self.stdscr.addstr(self.altura - 2, 2, "ESC para volver")
        self.stdscr.refresh()
        curses.echo()
        dni = self.menus._input_curses_utf8(3, 2, 20)
        curses.noecho()
        return dni
    
    def pedir_monto_cobrado(self):
        """
        Pide el monto cobrado.
        """
        while True:
            self.stdscr.clear()
            self.stdscr.addstr(1, 2, "Ingrese el monto cobrado (solo números, puede usar punto para decimales):")
            self.stdscr.addstr(self.altura - 2, 2, "ESC para cancelar")
            self.stdscr.move(3, 2)
            self.stdscr.clrtoeol()
            self.stdscr.refresh()
            curses.echo()
            monto_str = self.menus._input_curses_utf8(3, 2, 20)
            curses.noecho()
            if monto_str is None:
                return None
            monto_str = monto_str.replace(",", ".").strip()
            try:
                monto = float(monto_str)
                if monto < 0:
                    raise ValueError
                return monto
            except ValueError:
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(5, 2, "Monto inválido. Ingrese un número positivo.")
                self.stdscr.attroff(curses.color_pair(3))
                self.stdscr.refresh()
                curses.napms(1200) 

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
            nombre = self.menus._input_curses_utf8(6, x_form, 30)
            self.stdscr.move(fila_error, 0)
            self.stdscr.clrtoeol()
            if not nombre or not nombre.replace(' ', '').isalpha():
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
            telefono = self.menus._input_curses_utf8(9, x_form, 20)
            self.stdscr.move(fila_error, 0)
            self.stdscr.clrtoeol()
            if not telefono or not telefono.isdigit():
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
            documento = self.menus._input_curses_utf8(12, x_form, 20)
            self.stdscr.move(fila_error, 0)
            self.stdscr.clrtoeol()
            if not documento or not documento.isdigit():
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

    def confirmar_cancelacion(self, turno, documento):
        """
        Muestra un resumen del turno a cancelar y pide confirmación.
        Devuelve True si confirma, False si cancela la operación.
        """
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len("CONFIRMAR CANCELACIÓN")) // 2, "CONFIRMAR CANCELACIÓN")
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
            respuesta = self.menus._input_curses_utf8(y+4, 4, 5)
            if respuesta is None:
                curses.noecho()
                return False
            respuesta = respuesta.strip().lower()
            if respuesta.replace(' ', '') == "si":
                curses.noecho()
                return True
            elif respuesta.replace(' ', '') == "no":
                curses.noecho()
                return False
            else:
                error = True 

    def mostrar_detalles_reserva(self, reserva):
        """
        Muestra los detalles completos de una reserva seleccionada.
        """
        self.stdscr.clear()
        self.stdscr.attron(curses.color_pair(1))
        self.stdscr.addstr(1, (self.ancho - len("DETALLES DE RESERVA")) // 2, "DETALLES DE RESERVA")
        self.stdscr.attroff(curses.color_pair(1))
        
        y = 4
        fecha, hora = reserva["turno"]["fecha_hora"]
        
        # Información del turno
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(y, 4, "INFORMACIÓN DEL TURNO:")
        self.stdscr.attroff(curses.color_pair(2))
        y += 1
        self.stdscr.addstr(y, 6, f"Fecha: {fecha}")
        self.stdscr.addstr(y+1, 6, f"Hora: {hora}")
        self.stdscr.addstr(y+2, 6, f"Servicio: {reserva['turno']['servicio']}")
        self.stdscr.addstr(y+3, 6, f"Profesional: {reserva['turno']['profesional']}")
        y += 5
        
        # Información del cliente
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(y, 4, "INFORMACIÓN DEL CLIENTE:")
        self.stdscr.attroff(curses.color_pair(2))
        y += 1
        self.stdscr.addstr(y, 6, f"Nombre: {reserva['nombre']}")
        self.stdscr.addstr(y+1, 6, f"Teléfono: {reserva['telefono']}")
        self.stdscr.addstr(y+2, 6, f"DNI: {reserva['documento']}")
        y += 4
        
        # Estado y monto
        self.stdscr.attron(curses.color_pair(2))
        self.stdscr.addstr(y, 4, "ESTADO Y PAGO:")
        self.stdscr.attroff(curses.color_pair(2))
        y += 1
        
        estado = reserva.get("estado", "Pendiente")
        monto = reserva.get("montoCobrado")
        
        # Mostrar estado con color según el tipo
        if estado == "Atendida":
            self.stdscr.attron(curses.color_pair(1))  # Verde/Cyan
            self.stdscr.addstr(y, 6, f"Estado: {estado}")
            self.stdscr.attroff(curses.color_pair(1))
        elif estado == "No asistió":
            self.stdscr.attron(curses.color_pair(3))  # Rojo
            self.stdscr.addstr(y, 6, f"Estado: {estado}")
            self.stdscr.attroff(curses.color_pair(3))
        else:
            self.stdscr.attron(curses.color_pair(4))  # Amarillo
            self.stdscr.addstr(y, 6, f"Estado: {estado}")
            self.stdscr.attroff(curses.color_pair(4))
        
        y += 1
        
        if monto is not None:
            self.stdscr.attron(curses.color_pair(1))
            self.stdscr.addstr(y, 6, f"Monto cobrado: ${monto:.2f}")
            self.stdscr.attroff(curses.color_pair(1))
        else:
            if estado == "Atendida":
                self.stdscr.attron(curses.color_pair(3))
                self.stdscr.addstr(y, 6, "Monto cobrado: No registrado")
                self.stdscr.attroff(curses.color_pair(3))
            else:
                self.stdscr.addstr(y, 6, "Monto cobrado: Pendiente")
        
        # Instrucciones
        y += 3
        self.stdscr.attron(curses.color_pair(4))
        self.stdscr.addstr(y, 4, "Presione cualquier tecla para volver...")
        self.stdscr.attroff(curses.color_pair(4))
        
        self.stdscr.refresh()
        self.stdscr.getch() 