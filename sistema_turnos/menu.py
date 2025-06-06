from sistema_turnos.turnos import mostrar_turnos, filtrar_turnos, reservar_turnos, cancelar_turno
from sistema_turnos.clientes import ver_resumen_reservas, ver_nombre_clientes, ver_servicios_y_profesionales
from sistema_turnos.datos import guardar_reservas

def menu(turnos, reservas, rol):
    while True:
        print(f"\n=== MENÚ {rol.upper()} ===")
        
        if rol == "cliente":
            print("1. Ver turnos disponibles")
            print("2. Filtrar turnos")
            print("3. Reservar turno")
            print("4. Cancelar turno")
            print("5. Ver servicios y profesionales")
            print("0. Salir")
        elif rol == "manicurista":
            print("1. Ver resumen de reservas")
            print("2. Ver nombres de clientes")
            print("0. Salir")
            
        opcion = input("Seleccione una opción: ")

        if rol == "cliente":
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
                ver_servicios_y_profesionales(turnos)
            elif opcion == "0":
                print("Gracias por usar el sistema de turnos. ¡Hasta luego!")
                break
            else:
                print("Opción inválida")
                
        elif rol == "manicurista":
             if opcion == "1":
                 ver_resumen_reservas(reservas)
             elif opcion == "2":
                 ver_nombre_clientes(reservas)
             elif opcion == "0":
                 print("Gracias por usar el sistema de turnos. ¡Hasta luego!")
                 break
             else:
                print("Opción inválida")
