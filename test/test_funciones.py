import pytest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sistema_turnos.clientes import validar_documento, validar_nombre
from sistema_turnos.datos import cargar_turnos, guardar_turnos, agregar_turno
from sistema_turnos.turnos import filtrar_turnos, validar_fecha_hora

def test_validar_documento_valido():
    """
    Prueba que un documento válido sea aceptado.
    """
    assert validar_documento("12345678") == "12345678"

def test_validar_documento_invalido():
    """
    Prueba que un documento inválido sea rechazado.
    """
    with pytest.raises(ValueError):
        validar_documento("123abc")

def test_validar_nombre_valido():
    assert validar_nombre("Juan Perez") == "Juan Perez"

def test_validar_nombre_invalido():
    with pytest.raises(ValueError):
        validar_nombre("Juan123")

def test_validar_fecha_hora_valida():
    fecha, hora = validar_fecha_hora("01/01/2024", "14:30")
    assert fecha == "01/01/2024"
    assert hora == "14:30"

def test_validar_fecha_invalida():
    with pytest.raises(ValueError):
        validar_fecha_hora("2024/01/01", "14:30")

def test_validar_hora_invalida():
    with pytest.raises(ValueError):
        validar_fecha_hora("01/01/2024", "25:00")

def test_filtrar_por_servicio():
    """
    Prueba el filtrado de turnos por servicio.
    """
    turnos = cargar_turnos()
    filtrados = filtrar_turnos(turnos, servicio="Kapping")
    assert all(t["servicio"] == "Kapping" for t in filtrados)

def test_filtrar_por_profesional():
    """
    Prueba el filtrado de turnos por profesional.
    """
    turnos = cargar_turnos()
    filtrados = filtrar_turnos(turnos, profesional="Gisela")
    assert all(t["profesional"] == "Gisela" for t in filtrados)


def test_guardar_y_cargar_turnos():
    """
    Prueba que se puedan guardar y cargar turnos correctamente.
    """
    
    turnos_prueba = [
        {"fecha_hora": ["2025-04-26", "10:00"], "profesional": "Test", "servicio": "Test"}
    ]
    
   
    guardar_turnos(turnos_prueba)
    
    
    turnos_cargados = cargar_turnos()
    
    
    assert turnos_cargados == turnos_prueba

def test_agregar_turno():
    """
    Prueba que se pueda agregar un nuevo turno.
    """
   
    nuevo_turno = {
        "fecha_hora": ["2025-04-27", "15:00"],
        "profesional": "Test2",
        "servicio": "Test2"
    }
    
  
    agregar_turno(nuevo_turno)
    
    
    turnos = cargar_turnos()
    assert nuevo_turno in turnos

def test_manejo_errores_archivo_inexistente():
    """
    Prueba el manejo de errores cuando el archivo de turnos no existe.
    """
   
    if os.path.exists("turnos.json"):
        os.remove("turnos.json")
    
    
    turnos = cargar_turnos()
    assert isinstance(turnos, list)
    assert len(turnos)>0