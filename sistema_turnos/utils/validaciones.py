"""
Módulo de validaciones para el sistema de turnos.
Contiene funciones para validar documentos, datos de entrada, etc.
"""

import re

def validar_documento_recursivo(documento, posicion=0):
    """
    Valida que el documento tenga el formato correcto (DNI argentino) usando recursividad.
    FUNCIONALIDAD: Asegurar que los datos ingresados sean correctos usando recursividad
    RECURSIVIDAD: Reemplaza bucles tradicionales por llamadas recursivas
    """
    if not documento:
        raise ValueError("El documento no puede estar vacío")
    
    # Caso base: si llegamos al final del documento
    if posicion >= len(documento):
        # Verificar que tenga entre 7 y 8 dígitos
        if len(documento) < 7 or len(documento) > 8:
            raise ValueError("El documento debe tener 7 u 8 dígitos numéricos")
        return documento
    
    # Remover espacios y convertir a minúsculas en la primera llamada
    if posicion == 0:
        documento = documento.strip().lower()
    
    # Validar que el carácter en la posición actual sea un dígito
    if not documento[posicion].isdigit():
        raise ValueError(f"El carácter en la posición {posicion + 1} debe ser un dígito")
    
    # Llamada recursiva para validar el siguiente carácter
    return validar_documento_recursivo(documento, posicion + 1)

def validar_documento(documento):
    """
    Valida que el documento tenga el formato correcto (DNI argentino).
    """
    if not documento:
        raise ValueError("El documento no puede estar vacío")
    
    documento = documento.strip()
    
    # Verificar que solo contenga dígitos
    if not documento.isdigit():
        raise ValueError("El documento debe contener solo dígitos numéricos")
    
    # Verificar longitud (7 u 8 dígitos para DNI argentino)
    if len(documento) < 7 or len(documento) > 8:
        raise ValueError("El documento debe tener 7 u 8 dígitos numéricos")
    
    return documento

def validar_telefono(telefono):
    """
    Valida que el teléfono tenga el formato correcto.
    """
    if not telefono:
        raise ValueError("El teléfono no puede estar vacío")
    
    telefono = telefono.strip()
    
    # Remover espacios, guiones y paréntesis
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    
    # Verificar que solo contenga dígitos
    if not telefono_limpio.isdigit():
        raise ValueError("El teléfono debe contener solo dígitos numéricos")
    
    # Verificar longitud (10 dígitos para teléfonos argentinos)
    if len(telefono_limpio) != 10:
        raise ValueError("El teléfono debe tener 10 dígitos numéricos")
    
    return telefono_limpio

def validar_nombre(nombre):
    """
    Valida que el nombre tenga el formato correcto.
    """
    if not nombre:
        raise ValueError("El nombre no puede estar vacío")
    
    nombre = nombre.strip()
    
    # Verificar longitud mínima
    if len(nombre) < 2:
        raise ValueError("El nombre debe tener al menos 2 caracteres")
    
    # Verificar que solo contenga letras, espacios y algunos caracteres especiales
    if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre):
        raise ValueError("El nombre debe contener solo letras y espacios")
    
    return nombre.title() 