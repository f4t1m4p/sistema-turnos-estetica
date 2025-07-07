# Sistema de Turnos - Estructura Modular

## Descripción
Sistema de gestión de turnos para un negocio de manicuría, con funcionalidades para clientes y manicuristas.


### Arquitectura
```
AlgoritmosJueves/
├── main.py                        # Punto de entrada
├── iniciar_sistema.bat
├── sistema_turnos/
│   ├── __init__.py
│   ├── controlador_principal.py   # Controlador principal
│   ├── controlador/
│   │   ├── __init__.py
│   │   ├── cliente.py             # Funciones cliente
│   │   ├── manicurista.py         # Funciones manicurista
│   ├── interfaz/
│   │   ├── __init__.py
│   │   ├── menus.py               # Mostrar menús, entradas, etc.
│   │   ├── pantalla.py            # Limpieza, colores, helpers visuales
│   ├── logica/
│   │   ├── __init__.py
│   │   ├── reservas.py            # confirmar_reserva, cancelar, etc.
│   │   ├── atencion.py            # marcar_como_atendida, no_asistió, etc.
│   ├── datos/
│   │   ├── __init__.py
│   │   ├── persistencia.py        # cargar_turnos, guardar_turnos, etc.
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validaciones.py        # validar_documento, etc.
│   │   ├── filtros.py             # filtrar_turnos, etc.
├── test/
│   ├── test_cliente.py
│   ├── test_manicurista.py
│   ├── test_datos.py
├── reservas.json
├── turnos.json
├── sistema_turnos.log
```

### Módulos Principales

#### 1. Controlador Principal (`controlador_principal.py`)
- Coordina todos los subsistemas
- Maneja el flujo principal de la aplicación
- Inicializa controladores específicos

#### 2. Controladores Específicos
- **`controlador/cliente.py`**: Maneja operaciones de clientes
- **`controlador/manicurista.py`**: Maneja operaciones de manicuristas

#### 3. Interfaz Modular
- **`interfaz/menus.py`**: Menús de selección y navegación
- **`interfaz/pantalla.py`**: Presentación visual y helpers

#### 4. Lógica de Negocio
- **`logica/reservas.py`**: Reglas de negocio para reservas
- **`logica/atencion.py`**: Reglas de negocio para atención

#### 5. Datos
- **`datos/persistencia.py`**: Manejo de archivos JSON y backups

#### 6. Utilidades
- **`utils/validaciones.py`**: Validación de datos de entrada
- **`utils/filtros.py`**: Filtrado de información




## Funcionalidades Principales

### Para Clientes
- Ver turnos disponibles
- Filtrar turnos por servicio/profesional
- Reservar turnos
- Cancelar reservas
- Ver turnos reservados

### Para Manicuristas
- Ver resumen de reservas
- Gestionar reservas pendientes
- Marcar como atendida/no asistió
- Registrar montos cobrados
- Filtrar por estado

## Uso

```bash
# Ejecutar el sistema
python main.py

# Pruebas 
pytest

# O usar el batch file en Windows
iniciar_sistema.bat
```

## Archivos de Datos
- `turnos.json`: Turnos disponibles
- `reservas.json`: Reservas realizadas
- `sistema_turnos.log`: Log del sistema

## Notas 
- El sistema usa curses para interfaz de terminal
- Requiere terminal de mínimo 80x24 caracteres
- Compatible con Windows, Linux y macOS 