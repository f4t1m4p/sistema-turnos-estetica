"""
Módulo de validaciones para el sistema de turnos.
Contiene funciones para validar documentos, datos de entrada, etc.
"""

import re

def validar_documento(documento):
    """
    Valida que el documento tenga el formato correcto (DNI argentino).
    FUNCIONALIDAD: Asegurar que los datos ingresados sean correctos
    """
    if not documento:
        raise ValueError("El documento no puede estar vacío")
    
    # Remover espacios y convertir a minúsculas
    documento = documento.strip().lower()
    
    # Validar formato de DNI argentino (7-8 dígitos)
    if not re.match(r'^\d{7,8}$', documento):
        raise ValueError("El documento debe tener 7 u 8 dígitos numéricos")
    
    return documento

def validar_telefono(telefono):
    """
    Valida que el teléfono tenga el formato correcto.
    FUNCIONALIDAD: Asegurar que los datos ingresados sean correctos
    """
    if not telefono:
        raise ValueError("El teléfono no puede estar vacío")
    
    # Remover espacios y caracteres especiales
    telefono = re.sub(r'[^\d]', '', telefono)
    
    # Validar que tenga entre 10 y 15 dígitos
    if len(telefono) < 10 or len(telefono) > 15:
        raise ValueError("El teléfono debe tener entre 10 y 15 dígitos")
    
    return telefono

def validar_nombre(nombre):
    """
    Valida que el nombre tenga el formato correcto.
    FUNCIONALIDAD: Asegurar que los datos ingresados sean correctos
    """
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")
    
    # Remover espacios extra y capitalizar
    nombre = ' '.join(nombre.strip().split())
    
    # Validar que solo contenga letras y espacios
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
        raise ValueError("El nombre solo puede contener letras y espacios")
    
    if len(nombre) < 2:
        raise ValueError("El nombre debe tener al menos 2 caracteres")
    
    return nombre.title() 