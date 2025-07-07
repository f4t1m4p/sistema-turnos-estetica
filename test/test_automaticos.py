"""
Tests automáticos para la nueva estructura modular del sistema de turnos.
"""

import pytest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sistema_turnos.utils.validaciones import validar_documento, validar_telefono, validar_nombre
from sistema_turnos.utils.filtros import filtrar_turnos, filtrar_reservas_por_dni
from sistema_turnos.datos.persistencia import cargar_turnos, guardar_turnos, cargar_reservas, guardar_reservas
from sistema_turnos.logica.reservas import confirmar_reserva, crear_reserva
from sistema_turnos.logica.atencion import marcar_como_atendida, obtener_estadisticas_reservas

def test_validar_documento_valido():
    assert validar_documento("12345678") == "12345678"

def test_validar_documento_invalido():
    with pytest.raises(ValueError):
        validar_documento("123abc")

def test_validar_telefono_valido():
    assert validar_telefono("1234567890") == "1234567890"

def test_validar_telefono_invalido():
    with pytest.raises(ValueError):
        validar_telefono("123")

def test_validar_nombre_valido():
    assert validar_nombre("Juan Perez") == "Juan Perez"

def test_validar_nombre_invalido():
    with pytest.raises(ValueError):
        validar_nombre("Juan123")

def test_filtrar_turnos_por_servicio():
    turnos = [
        {"fecha_hora": ["2025-07-01", "09:00"], "profesional": "Marisol", "servicio": "Kapping"},
        {"fecha_hora": ["2025-07-01", "13:30"], "profesional": "Marisol", "servicio": "Semi"}
    ]
    filtrados = filtrar_turnos(turnos, servicio="kapping")
    assert len(filtrados) == 1
    assert filtrados[0]["servicio"] == "Kapping"

def test_filtrar_turnos_por_profesional():
    turnos = [
        {"fecha_hora": ["2025-07-01", "09:00"], "profesional": "Marisol", "servicio": "Kapping"},
        {"fecha_hora": ["2025-07-01", "13:30"], "profesional": "Gisela", "servicio": "Semi"}
    ]
    filtrados = filtrar_turnos(turnos, profesional="marisol")
    assert len(filtrados) == 1
    assert filtrados[0]["profesional"] == "Marisol"

def test_filtrar_reservas_por_dni():
    reservas = [
        {"documento": "12345678", "nombre": "Juan", "turno": {}},
        {"documento": "87654321", "nombre": "Ana", "turno": {}}
    ]
    filtradas = filtrar_reservas_por_dni(reservas, "12345678")
    assert len(filtradas) == 1
    assert filtradas[0]["documento"] == "12345678"

def test_confirmar_reserva_valida():
    turno = {"fecha_hora": ["2025-07-01", "09:00"], "profesional": "Marisol", "servicio": "Kapping"}
    resultado = confirmar_reserva(turno, "Juan Perez", "1234567890", "12345678")
    assert resultado["valido"] == True
    assert resultado["nombre"] == "Juan Perez"

def test_confirmar_reserva_invalida():
    turno = {"fecha_hora": ["2025-07-01", "09:00"], "profesional": "Marisol", "servicio": "Kapping"}
    resultado = confirmar_reserva(turno, "Juan123", "1234567890", "12345678")
    assert resultado["valido"] == False
    assert "error" in resultado

def test_crear_reserva_exitosa():
    turno = {"fecha_hora": ["2025-07-01", "09:00"], "profesional": "Marisol", "servicio": "Kapping"}
    reservas = []
    resultado = crear_reserva(turno, "Juan Perez", "1234567890", "12345678", reservas)
    assert resultado["exito"] == True
    assert resultado["reserva"]["nombre"] == "Juan Perez"

def test_crear_reserva_duplicada():
    turno = {"fecha_hora": ["2025-07-01", "09:00"], "profesional": "Marisol", "servicio": "Kapping"}
    reservas = [{"documento": "12345678", "nombre": "Juan", "turno": {}}]
    resultado = crear_reserva(turno, "Juan Perez", "1234567890", "12345678", reservas)
    assert resultado["exito"] == False
    assert "error" in resultado

def test_marcar_como_atendida():
    reserva = {"nombre": "Juan", "estado": "Pendiente"}
    reservas = [reserva]
    resultado = marcar_como_atendida(reserva, reservas)
    assert resultado["exito"] == True
    assert reserva["estado"] == "Atendida"

def test_obtener_estadisticas_reservas():
    reservas = [
        {"estado": "Pendiente", "montoCobrado": None},
        {"estado": "Atendida", "montoCobrado": 100},
        {"estado": "No asistió", "montoCobrado": None}
    ]
    stats = obtener_estadisticas_reservas(reservas)
    assert stats["total_reservas"] == 3
    assert stats["pendientes"] == 1
    assert stats["atendidas"] == 1
    assert stats["no_asistieron"] == 1
    assert stats["ingresos_totales"] == 100

def test_cargar_y_guardar_turnos():
    turnos_prueba = [
        {"fecha_hora": ["2025-07-01", "10:00"], "profesional": "Test", "servicio": "Test"}
    ]
    guardar_turnos(turnos_prueba)
    turnos_cargados = cargar_turnos()
    assert len(turnos_cargados) >= 1
    assert any(t["profesional"] == "Test" for t in turnos_cargados)

def test_cargar_y_guardar_reservas():
    reservas_prueba = [
        {"documento": "12345678", "nombre": "Test", "turno": {}, "estado": "Pendiente"}
    ]
    guardar_reservas(reservas_prueba)
    reservas_cargadas = cargar_reservas()
    assert len(reservas_cargadas) >= 1
    assert any(r["documento"] == "12345678" for r in reservas_cargadas) 