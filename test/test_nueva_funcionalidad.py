"""
Test para la nueva funcionalidad de selección de reservas en el resumen.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sistema_turnos.logica.reservas import confirmar_reserva

def test_confirmar_reserva_mensajes_especificos():
    """
    Test que verifica que los mensajes de error son específicos para cada campo.
    """
    # Test con DNI inválido
    turno = {"fecha_hora": ["2025-07-01", "09:00"], "profesional": "Marisol", "servicio": "Kapping"}
    resultado = confirmar_reserva(turno, "Juan", "1234567890", "123abc")
    assert resultado["valido"] == False
    assert "Error en el DNI:" in resultado["error"]
    
    # Test con teléfono inválido
    resultado = confirmar_reserva(turno, "Juan", "123", "12345678")
    assert resultado["valido"] == False
    assert "Error en el teléfono:" in resultado["error"]
    
    # Test con nombre inválido
    resultado = confirmar_reserva(turno, "Juan123", "1234567890", "12345678")
    assert resultado["valido"] == False
    assert "Error en el nombre:" in resultado["error"]
    
    # Test con datos válidos
    resultado = confirmar_reserva(turno, "Juan", "1234567890", "12345678")
    assert resultado["valido"] == True
    assert "error" not in resultado

if __name__ == "__main__":
    print("Ejecutando tests de nueva funcionalidad...")
    test_confirmar_reserva_mensajes_especificos()
    print("✓ Todos los tests pasaron correctamente!") 