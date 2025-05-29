# === ENTORNOS DE DESARROLLO ===
import os
from functools import reduce

ENTORNO = os.getenv("ENTORNO", "desarrollo")
if ENTORNO == "produccion":
    print("⚠ Ejecutando en entorno de PRODUCCIÓN")
else:
    print("🛠 Ejecutando en entorno de DESARROLLO")

# === FUNCIONES DEL SISTEMA ===

def cargar_turnos():
    return [
        {"fecha_hora": ("2025-04-26", "10:00"), "profesional": "Gisela", "servicio": "Kapping"},
        {"fecha_hora": ("2025-04-25", "14:00"), "profesional": "Marisol", "servicio": "Semi"},
        {"fecha_hora": ("2025-04-26", "16:00"), "profesional": "Valentina", "servicio": "Soft Gel"},
    ]

def filtrar_turnos(turnos, servicio=None, profesional=None):
    return list(filter(lambda t:
        (servicio is None or t['servicio'] == servicio) and
        (profesional is None or t['profesional'] == profesional),
        turnos
    ))

def mostrar_turnos(turnos):
    print("\nTurnos disponibles:")
    for i, turno in enumerate(turnos):
        fecha, hora = turno["fecha_hora"]
        print(f"{i + 1}. {fecha} {hora} - {turno['servicio']} con {turno['profesional']}")

def validar_documento(documento):
    if not documento.isdigit():
        raise ValueError("El documento debe contener solo números.")

def reservar_turnos(turnos, reservas):
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
        validar_documento(documento)

        cliente = {
            "nombre": nombre,
            "telefono": telefono,
            "documento": documento,
            "turno": turno,
        }
        reservas.append(cliente)
        turnos = [t for t in turnos if t != turno]
    except ValueError as e:
        print(f"Error: {e}")
    else:
        print(f"\nTurno reservado con éxito para {nombre}!")
    finally:
        print("Fin del intento de reserva.")

    return turnos, reservas

def cancelar_turno(turnos, reservas):
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

    return turnos, nuevas_reservas

def ver_resumen_reservas(reservas):
    resumen = {}
    for r in reservas:
        profesional = r["turno"]["profesional"]
        resumen.setdefault(profesional, []).append(r)

    print("\n--- Resumen de Reservas ---")
    for profesional, lista in resumen.items():
        print(f"\nTurnos de {profesional}:")
        for r in lista:
            fecha, hora = r["turno"]["fecha_hora"]
            print(f"- {r['nombre']} el {fecha} a las {hora} para {r['turno']['servicio']}")
    print(f"\nTotal de reservas: {len(reservas)}")

def ver_nombre_clientes(reservas):
    nombres = {r["nombre"] for r in reservas}
    print("Clientes con turnos reservados:")
    for nombre in nombres:
        print(f"- {nombre}")

def ver_servicios_y_profesionales(turnos):
    servicios = set(t["servicio"] for t in turnos)
    profesionales = set(t["profesional"] for t in turnos)
    print("\nServicios disponibles:", ', '.join(servicios))
    print("Profesionales disponibles:", ', '.join(profesionales))

def menu(turnos, reservas):
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Ver turnos disponibles")
        print("2. Filtrar turnos")
        print("3. Reservar turno")
        print("4. Cancelar turno")
        print("5. Ver resumen de reservas")
        print("6. Ver nombres de clientes")
        print("7. Ver servicios y profesionales")
        print("0. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_turnos(turnos)
        elif opcion == "2":
            servicio = input("Filtrar por servicio (Kapping, Semi, Soft Gel o ENTER): ").strip() or None
            profesional = input("Filtrar por profesional (Gisela, Marisol, Valentina o ENTER): ").strip() or None
            filtrados = filtrar_turnos(turnos, servicio, profesional)
            mostrar_turnos(filtrados)
        elif opcion == "3":
            turnos, reservas = reservar_turnos(turnos, reservas)
        elif opcion == "4":
            turnos, reservas = cancelar_turno(turnos, reservas)
        elif opcion == "5":
            ver_resumen_reservas(reservas)
        elif opcion == "6":
            ver_nombre_clientes(reservas)
        elif opcion == "7":
            ver_servicios_y_profesionales(turnos)
        elif opcion == "0":
            print("Gracias por usar el sistema de turnos. ¡Hasta luego!")
            break
        else:
            print("Opción inválida")

# === FUNCIÓN PRINCIPAL ===
def main():
    turnos = cargar_turnos()
    reservas = []
    menu(turnos, reservas)

if __name__ == "__main__":
    main()

# === PRUEBAS UNITARIAS CON PYTEST ===

def test_validar_documento_valido():
    assert validar_documento("12345678") is None

def test_validar_documento_invalido():
    import pytest
    with pytest.raises(ValueError):
        validar_documento("abc123")

def test_filtrar_por_servicio():
    turnos = cargar_turnos()
    filtrados = filtrar_turnos(turnos, servicio="Kapping")
    assert all(t["servicio"] == "Kapping" for t in filtrados)

def test_filtrar_por_profesional():
    turnos = cargar_turnos()
    filtrados = filtrar_turnos(turnos, profesional="Gisela")
    assert all(t["profesional"] == "Gisela" for t in filtrados)
