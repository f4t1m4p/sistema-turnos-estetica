from sistema_turnos.turnos import mostrar_turnos, filtrar_turnos, reservar_turnos, cancelar_turno
from sistema_turnos.clientes import ver_resumen_reservas, ver_nombre_clientes, ver_servicios_y_profesionales

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
