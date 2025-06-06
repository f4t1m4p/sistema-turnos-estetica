import pytest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(_file_), '..')))

from sistema_turnos.clientes import validar_documento
from sistema_turnos.datos import cargar_turnos, guardar_turnos, agregar_turno
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


def test_guardar_y_cargar_turnos():
    
    turnos_prueba = [
        {"fecha_hora": ["2025-04-26", "10:00"], "profesional": "Test", "servicio": "Test"}
    ]
    
   
    guardar_turnos(turnos_prueba)
    
    
    turnos_cargados = cargar_turnos()
    
    
    assert turnos_cargados == turnos_prueba

def test_agregar_turno():
   
    nuevo_turno = {
        "fecha_hora": ["2025-04-27", "15:00"],
        "profesional": "Test2",
        "servicio": "Test2"
    }
    
  
    agregar_turno(nuevo_turno)
    
    
    turnos = cargar_turnos()
    assert nuevo_turno in turnos

def test_manejo_errores_archivo_inexistente():
   
    if os.path.exists("turnos.json"):
        os.remove("turnos.json")
    
    
    turnos = cargar_turnos()
    assert isinstance(turnos, list)
    assert len(turnos)>0