"""
Tests básicos para la nueva estructura modular del sistema de turnos.
"""

import pytest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sistema_turnos.utils.validaciones import (
    validar_documento, validar_telefono, validar_nombre,
    validar_documento_recursivo
)
from sistema_turnos.utils.filtros import filtrar_turnos, filtrar_reservas_por_dni
from sistema_turnos.datos.persistencia import cargar_turnos, guardar_turnos, cargar_reservas, guardar_reservas
from sistema_turnos.logica.reservas import confirmar_reserva, crear_reserva
from sistema_turnos.logica.atencion import marcar_como_atendida, obtener_estadisticas_reservas

def test_validar_documento_valido():
    """Prueba que un documento válido sea aceptado."""
    assert validar_documento("12345678") == "12345678"

def test_validar_documento_invalido():
    """Prueba que un documento inválido sea rechazado."""
    with pytest.raises(ValueError):
        validar_documento("123abc")

# Tests para función recursiva de validación de documento
def test_validar_documento_recursivo_valido():
    """Prueba que un documento válido sea aceptado por la función recursiva."""
    assert validar_documento_recursivo("12345678") == "12345678"
    assert validar_documento_recursivo("1234567") == "1234567"

def test_validar_documento_recursivo_invalido():
    """Prueba que un documento inválido sea rechazado por la función recursiva."""
    with pytest.raises(ValueError):
        validar_documento_recursivo("123abc")
    with pytest.raises(ValueError):
        validar_documento_recursivo("123456")  # Muy corto
    with pytest.raises(ValueError):
        validar_documento_recursivo("123456789")  # Muy largo 