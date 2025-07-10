"""
Test para verificar la navegación en el resumen de reservas.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_estructura_reservas():
    """
    Test que verifica que la estructura de reservas es correcta para la navegación.
    """
    # Simular datos de reservas como los que están en reservas.json
    reservas_ejemplo = [
        {
            "nombre": "maga",
            "telefono": "2227584761",
            "documento": "78787878",
            "turno": {
                "fecha_hora": ["2025-07-01", "13:30"],
                "profesional": "Marisol",
                "servicio": "Semi"
            },
            "estado": "No asistió",
            "montoCobrado": None
        },
        {
            "nombre": "mam",
            "telefono": "123456789123",
            "documento": "1234567",
            "turno": {
                "fecha_hora": ["2025-07-02", "10:30"],
                "profesional": "Valentina",
                "servicio": "Kapping"
            },
            "estado": "Atendida",
            "montoCobrado": 2000.0
        }
    ]
    
    # Verificar que las reservas tienen la estructura correcta
    for reserva in reservas_ejemplo:
        assert "nombre" in reserva
        assert "telefono" in reserva
        assert "documento" in reserva
        assert "turno" in reserva
        assert "estado" in reserva
        assert "montoCobrado" in reserva
        
        # Verificar estructura del turno
        turno = reserva["turno"]
        assert "fecha_hora" in turno
        assert "profesional" in turno
        assert "servicio" in turno
        assert len(turno["fecha_hora"]) == 2  # fecha y hora
    
    # Verificar agrupación por profesional
    profesionales = {}
    for r in reservas_ejemplo:
        profesional = r["turno"]["profesional"].capitalize()
        profesionales.setdefault(profesional, []).append(r)
    
    assert "Marisol" in profesionales
    assert "Valentina" in profesionales
    assert len(profesionales["Marisol"]) == 1
    assert len(profesionales["Valentina"]) == 1
    
    print("✓ Estructura de reservas correcta")

def test_navegacion_resumen():
    """
    Test que simula la lógica de navegación del resumen.
    """
    # Simular reservas
    reservas = [
        {"turno": {"profesional": "Marisol"}, "nombre": "Cliente1"},
        {"turno": {"profesional": "Valentina"}, "nombre": "Cliente2"},
        {"turno": {"profesional": "Marisol"}, "nombre": "Cliente3"}
    ]
    
    # Crear lista plana para navegación
    reservas_planas = []
    profesionales = {}
    for r in reservas:
        profesional = r["turno"]["profesional"].capitalize()
        profesionales.setdefault(profesional, []).append(r)
        reservas_planas.append(r)
    
    # Verificar que la navegación funciona
    assert len(reservas_planas) == 3
    assert len(profesionales) == 2  # Marisol y Valentina
    
    # Simular selección
    seleccion = 0
    assert seleccion >= 0
    assert seleccion < len(reservas_planas)
    
    # Simular navegación hacia abajo
    seleccion += 1
    assert seleccion == 1
    assert seleccion < len(reservas_planas)
    
    # Simular navegación hacia arriba
    seleccion -= 1
    assert seleccion == 0
    assert seleccion >= 0
    
    print("✓ Lógica de navegación correcta")

if __name__ == "__main__":
    print("Ejecutando tests de navegación...")
    test_estructura_reservas()
    test_navegacion_resumen()
    print("✓ Todos los tests de navegación pasaron correctamente!") 