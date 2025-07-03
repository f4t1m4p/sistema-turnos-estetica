"""
Controlador principal del sistema de turnos.
Maneja la coordinación entre la interfaz y la lógica de negocio.
"""

import curses
from sistema_turnos.datos import cargar_turnos, cargar_reservas, guardar_reservas, guardar_turnos
from sistema_turnos.turnos import mostrar_turnos, filtrar_turnos, reservar_turnos, cancelar_turno
from sistema_turnos.clientes import ver_resumen_reservas, ver_nombre_clientes, validar_documento

class ControladorTurnos:
    """
    Controlador principal que coordina la interfaz con la lógica de negocio.
    """
    
    def __init__(self, interfaz):
        self.interfaz = interfaz
        self.turnos = cargar_turnos()
        self.reservas = cargar_reservas()
    
    def ejecutar(self):
        """
        Método principal que ejecuta el sistema.
        """
        while True:
            opcion = self.interfaz.mostrar_menu_principal()
            
            if opcion == 0:  
                self.ejecutar_menu_cliente()
            elif opcion == 1:  
                self.ejecutar_menu_manicurista()
            elif opcion == 2:  
                self.interfaz.mostrar_mensaje("Gracias por usar el sistema de turnos. ¡Hasta luego!")
                break
    
    def ejecutar_menu_cliente(self):
        """
        Maneja el menú de cliente.
        """
        while True:
            opcion_cliente = self.interfaz.menu_cliente()
            
            if opcion_cliente == 0:  
                self.interfaz.reservar_turno_columna_lateral(self.turnos, solo_vista=True)
            elif opcion_cliente == 1: 
                self.filtrar_turnos_cliente()
            elif opcion_cliente == 2:  
                self.reservar_turno_cliente()
            elif opcion_cliente == 3: 
                self.cancelar_turno_cliente()
            elif opcion_cliente == 4:  
                self.ver_turnos_reservados_cliente()
            elif opcion_cliente == 5:  
                break
    
    def ejecutar_menu_manicurista(self):
        """
        Maneja el menú de manicurista.
        """
        while True:
            opcion_manicurista = self.interfaz.menu_manicurista()
            
            if opcion_manicurista == 0:  
                self.interfaz.mostrar_resumen_reservas(self.reservas)
            elif opcion_manicurista == 1: 
                self.gestionar_reservas_pendientes()
            elif opcion_manicurista == 2:  
                self.filtrar_turnos_manicurista()
            elif opcion_manicurista == 3: 
                break
    
    def filtrar_turnos_cliente(self):
        """
        Maneja el filtrado de turnos para clientes.
        """
        opciones_servicio = ["kapping", "semi", "soft gel"]
        opciones_profesional = ["gisela", "marisol", "valentina"]
        
      
        servicio = self._pedir_filtro_servicio(opciones_servicio)
        if servicio is None:
            return
        
       
        profesional = self._pedir_filtro_profesional(opciones_profesional)
        if profesional is None:
            return
        
        
        filtrados = filtrar_turnos(self.turnos, servicio, profesional)
        self.interfaz.mostrar_turnos(filtrados)
    
    def _pedir_filtro_servicio(self, opciones_servicio):
        """
        Pide al usuario que ingrese un filtro de servicio.
        """
        while True:
            self.interfaz.stdscr.clear()
            self.interfaz.stdscr.addstr(1, 2, "Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ")
            self.interfaz.stdscr.addstr(self.interfaz.altura - 2, 2, "ESC para volver")
            if 'error_servicio' in locals() and error_servicio:
                self.interfaz.stdscr.attron(curses.color_pair(3))
                self.interfaz.stdscr.addstr(2, 2, "Servicio inválido. Opciones: Kapping, Semi, Soft Gel.")
                self.interfaz.stdscr.attroff(curses.color_pair(3))
            self.interfaz.stdscr.move(3, 2)
            self.interfaz.stdscr.clrtoeol()
            self.interfaz.stdscr.refresh()
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
    
    def _pedir_filtro_profesional(self, opciones_profesional):
        """
        Pide al usuario que ingrese un filtro de profesional.
        """
        while True:
            self.interfaz.stdscr.clear()
            self.interfaz.stdscr.addstr(1, 2, "Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ")
            self.interfaz.stdscr.addstr(self.interfaz.altura - 2, 2, "ESC para volver")
            if 'error_prof' in locals() and error_prof:
                self.interfaz.stdscr.attron(curses.color_pair(3))
                self.interfaz.stdscr.addstr(2, 2, "Profesional inválido. Opciones: Gisela, Marisol, Valentina.")
                self.interfaz.stdscr.attroff(curses.color_pair(3))
            self.interfaz.stdscr.move(3, 2)
            self.interfaz.stdscr.clrtoeol()
            self.interfaz.stdscr.refresh()
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
    
    def reservar_turno_cliente(self):
        """
        Maneja la reserva de turnos para clientes.
        """
        resultado = self.interfaz.reservar_turno_columna_lateral(self.turnos)
        if resultado is None:
            return
        
        opcion, nombre, telefono, documento = resultado
        
        try:
            turno = self.turnos[opcion]
            validar_documento(documento)
            
            
            if any(r["documento"].lower() == documento.lower() for r in self.reservas):
                self.interfaz.mostrar_mensaje("Ya hay un turno reservado con este DNI.", "error")
                return
            
            if not self.interfaz.confirmar_reserva(turno, nombre, telefono, documento):
                return
            
           
            cliente = {
                "nombre": nombre,
                "telefono": telefono,
                "documento": documento,
                "turno": turno,
                "estado": "Pendiente",
                "montoCobrado": None
            }
            
            self.reservas.append(cliente)
            self.turnos = [t for t in self.turnos if t != turno]
            
            
            guardar_reservas(self.reservas)
            guardar_turnos(self.turnos)
            
            
            self.turnos = cargar_turnos()
            self.reservas = cargar_reservas()
            
            self.interfaz.mostrar_mensaje(f"Turno reservado con éxito para {nombre}!", "exito")
            
        except (ValueError, IndexError) as e:
            self.interfaz.mostrar_mensaje(f"Error: {str(e)}", "error")
    
    def cancelar_turno_cliente(self):
        """
        Maneja la cancelación de turnos para clientes.
        """
        
        while True:
            self.interfaz.stdscr.clear()
            prompt = "Ingrese su documento para cancelar el turno: "
            self.interfaz.stdscr.addstr(1, 2, prompt)
            self.interfaz.stdscr.addstr(self.interfaz.altura - 2, 2, "Presione ESC para volver")
            if 'error_doc' in locals() and error_doc:
                self.interfaz.stdscr.attron(curses.color_pair(3))
                self.interfaz.stdscr.addstr(3, 2, "El documento debe contener solo números.")
                self.interfaz.stdscr.attroff(curses.color_pair(3))
            self.interfaz.stdscr.move(2, 2)
            self.interfaz.stdscr.clrtoeol()
            self.interfaz.stdscr.refresh()
            curses.echo()
            documento = self._input_curses_utf8(2, 2, 20)
            curses.noecho()
            
            if documento is None:
                return
            
            if documento == "":
                continue
            
            if not documento.isdigit():
                error_doc = True
                continue
            
            break
        
       
        nuevas_reservas = []
        turno_recuperado = None
        
        for r in self.reservas:
            if r["documento"].lower() == documento.lower():
                turno_recuperado = r["turno"]
            else:
                nuevas_reservas.append(r)
        
        if turno_recuperado:
            if self.interfaz.confirmar_cancelacion(turno_recuperado, documento):
                self.turnos.append(turno_recuperado)
                self.reservas = nuevas_reservas
                
                
                guardar_reservas(self.reservas)
                guardar_turnos(self.turnos)
                
                
                self.turnos = cargar_turnos()
                self.reservas = cargar_reservas()
                
                self.interfaz.mostrar_mensaje("Turno cancelado correctamente.", "exito")
            else:
                self.interfaz.mostrar_mensaje("Cancelación abortada.", "info")
        else:
            self.interfaz.mostrar_mensaje("No se encontró una reserva con ese documento.", "error")
    
    def ver_turnos_reservados_cliente(self):
        """
        Muestra los turnos reservados del cliente.
        """
        while True:
            self.interfaz.stdscr.clear()
            prompt = "Ingrese su documento para ver sus turnos: "
            self.interfaz.stdscr.addstr(1, 2, prompt)
            self.interfaz.stdscr.addstr(self.interfaz.altura - 2, 2, "Presione ESC para volver")
            if 'error_doc' in locals() and error_doc:
                self.interfaz.stdscr.attron(curses.color_pair(3))
                self.interfaz.stdscr.addstr(3, 2, "El documento debe contener solo números.")
                self.interfaz.stdscr.attroff(curses.color_pair(3))
            self.interfaz.stdscr.move(2, 2)
            self.interfaz.stdscr.clrtoeol()
            self.interfaz.stdscr.refresh()
            curses.echo()
            documento = self._input_curses_utf8(2, 2, 20)
            curses.noecho()
            
            if documento is None:
                return
            
            if documento == "":
                continue
            
            if not documento.isdigit():
                error_doc = True
                continue
            
            break
        
        
        def coincide(r):
            return r["documento"].lower() == documento.lower()
        
        reservas_cliente = [r for r in self.reservas if coincide(r)]
        
        if reservas_cliente:
            self.interfaz.mostrar_turnos_reservados(reservas_cliente, documento)
        else:
            self.interfaz.mostrar_mensaje("No se encontraron reservas con ese documento.", "info")
    
    def gestionar_reservas_pendientes(self):
        """
        Maneja la gestión de reservas pendientes para manicuristas.
        """
        reservas_pendientes = [r for r in self.reservas if r["estado"] == "Pendiente"]
        
        if not reservas_pendientes:
            self.interfaz.mostrar_mensaje("No hay reservas pendientes.", "info")
            return
        
        self.interfaz.gestionar_reservas_pendientes(reservas_pendientes)
        
        
        self.reservas = cargar_reservas()
    
    def filtrar_turnos_manicurista(self):
        """
        Maneja el filtrado de turnos para manicuristas.
        """
        opciones_estado = ["pendiente", "atendido", "no asistió", "no asistio"]
        opciones_servicio = ["kapping", "semi", "soft gel"]
        opciones_profesional = ["gisela", "marisol", "valentina"]
        
       
        estado = self._pedir_filtro_estado(opciones_estado)
        if estado is None:
            return
        
        
        servicio = self._pedir_filtro_servicio(opciones_servicio)
        if servicio is None:
            return
        
        
        profesional = self._pedir_filtro_profesional(opciones_profesional)
        if profesional is None:
            return
        
        
        def coincide(r):
            if estado and r.get('estado', 'Pendiente').lower() != estado:
                return False
            if servicio and r['turno']['servicio'].lower() != servicio:
                return False
            if profesional and r['turno']['profesional'].lower() != profesional:
                return False
            return True
        
        filtradas = sorted(filter(coincide, self.reservas), 
                          key=lambda r: (r['turno']['fecha_hora'][0], r['turno']['fecha_hora'][1]))
        
        self.interfaz.mostrar_lista_reservas_navegable(filtradas)
    
    def _pedir_filtro_estado(self, opciones_estado):
        """
        Pide al usuario que ingrese un filtro de estado.
        """
        while True:
            self.interfaz.stdscr.clear()
            self.interfaz.stdscr.addstr(1, 2, "Filtrar por estado (Pendiente, Atendido, No asistió o ENTER): ")
            self.interfaz.stdscr.addstr(self.interfaz.altura - 2, 2, "ESC para volver")
            if 'error_estado' in locals() and error_estado:
                self.interfaz.stdscr.attron(curses.color_pair(3))
                self.interfaz.stdscr.addstr(2, 2, "Estado inválido. Opciones: Pendiente, Atendido, No asistió.")
                self.interfaz.stdscr.attroff(curses.color_pair(3))
            self.interfaz.stdscr.move(3, 2)
            self.interfaz.stdscr.clrtoeol()
            self.interfaz.stdscr.refresh()
            curses.echo()
            estado = self._input_curses_utf8(3, 2, 50)
            curses.noecho()
            
            if estado is None:
                return None
            
            estado = estado.lower()
            if estado == "":
                return None
            
            if not estado.replace(" ", "").isalpha() or estado not in opciones_estado:
                error_estado = True
                continue
            
            return estado
    
    def _input_curses_utf8(self, y, x, maxlen=50):
        """
        Función auxiliar para input con soporte UTF-8.
        """
        buffer = bytearray()
        while True:
            ch = self.interfaz.stdscr.getch(y, x + len(buffer.decode('utf-8', errors='ignore')))
            if ch == 27: 
                return None
            elif ch in (10, 13):  
                break
            elif ch in (8, 127): 
                if buffer:
                    buffer = buffer[:-1]
                    self.interfaz.stdscr.move(y, x + len(buffer.decode('utf-8', errors='ignore')))
                    self.interfaz.stdscr.delch()
            else:
                
                if 0 <= ch <= 255:
                    buffer += bytes([ch])
                    try:
                        self.interfaz.stdscr.addstr(y, x, buffer.decode('utf-8', errors='ignore'))
                    except Exception:
                        pass
                
        return buffer.decode('utf-8', errors='ignore').strip() 