import re
from sistema_turnos.datos import guardar_reservas

def validar_fecha_hora(fecha, hora):
    """
    Valida el formato de fecha y hora.
    """
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', fecha):
        raise ValueError("Formato de fecha inválido (DD/MM/AAAA)")
    if not re.match(r'^\d{2}:\d{2}$', hora):
        raise ValueError("Formato de hora inválido (HH:MM)")
    
    # Validar rangos de hora y minutos
    horas, minutos = map(int, hora.split(':'))
    if horas < 0 or horas > 23:
        raise ValueError("Las horas deben estar entre 0 y 23")
    if minutos < 0 or minutos > 59:
        raise ValueError("Los minutos deben estar entre 0 y 59")
    
    return fecha, hora

def mostrar_turnos(turnos):
    """
    Muestra los turnos disponibles.
    """
    print("\nTurnos disponibles:")
    for i, turno in enumerate(turnos):
        fecha, hora = turno["fecha_hora"]
        print(f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}")

def filtrar_turnos(turnos, servicio=None, profesional=None):
    """
    Filtra los turnos por servicio o profesional.
    """
    return list(filter(lambda t:
        (servicio is None or t['servicio'] == servicio) and
        (profesional is None or t['profesional'] == profesional),
        turnos
    ))

def reservar_turnos(turnos, reservas):
    """
    Reserva un turno.
    """
    mostrar_turnos(turnos)
    nombres_existentes = {r["nombre"] for r in reservas}

    try:
        opcion = int(input("\nElija el número del turno que desea reservar: ")) - 1
        turno = turnos[opcion]
    except (ValueError, IndexError) as e:
        print(f"Error al seleccionar turno: {e}")
        return turnos, reservas

    try:
        nombre = input("Ingrese su nombre: ")
        if nombre in nombres_existentes:
            raise ValueError("Ya existe una reserva con ese nombre.")

        telefono = input("Ingrese su teléfono: ")
        documento = input("Ingrese su documento: ")
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
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print(f"\nTurno reservado con éxito para {nombre}!")
    finally:
        print("Fin del intento de reserva.")

    return turnos, reservas

def cancelar_turno(turnos, reservas):
    """
    Cancela un turno reservado.
    """
    documento = input("Ingrese su documento para cancelar el turno: ")
    nuevas_reservas = []
    turno_recuperado = None

    for r in reservas:
        if r["documento"].lower() == documento.lower():
            turno_recuperado = r["turno"]
            print("Turno cancelado correctamente.")
        else:
            nuevas_reservas.append(r)

    if turno_recuperado:
        turnos.append(turno_recuperado)
    else:
        print("No se encontró una reserva con ese documento.")
        
    guardar_reservas(nuevas_reservas)

    return turnos, nuevas_reservas
