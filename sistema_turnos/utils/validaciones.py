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