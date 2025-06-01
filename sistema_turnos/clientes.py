def validar_documento(documento):
    if not documento.isdigit():
        raise ValueError("El documento debe contener solo números.")

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
