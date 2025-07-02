@echo off
REM ========== Sistema de Gestión de Turnos - Estética Aura ==========
REM Este archivo ejecuta el sistema principal del proyecto.

REM Si usás entorno virtual, descomenta la siguiente línea:
REM call venv\Scripts\activate

REM Si necesitás instalar dependencias, descomenta la siguiente línea:
REM pip install -r requirements.txt

REM Instalar windows-curses si hace falta (solo en Windows)
pip install windows-curses >nul 2>&1

REM Ejecutar el sistema principal
python main.py

REM Mantener la ventana abierta al finalizar
pause 