@echo off
title Reciclap - Reporte de Pruebas
cd /d "%~dp0"

echo ========================================
echo  Generando reporte de pruebas Reciclap
echo ========================================
echo.

:: Activar entorno virtual
call venv\Scripts\activate.bat

:: Ejecutar script que hace pytest + unión de reportes
python generar_reporte_completo.py

:: Abrir el reporte combinado en el navegador
start reporte_completo.html

pause