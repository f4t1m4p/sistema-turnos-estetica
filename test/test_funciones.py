import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sistema_turnos.clientes import validar_documento
from sistema_turnos.datos import cargar_turnos
from sistema_turnos.turnos import filtrar_turnos

def test_validar_documento_valido():
    assert validar_documento("12345678") is None

def test_validar_documento_invalido():
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
