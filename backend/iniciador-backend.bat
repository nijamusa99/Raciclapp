@echo off
title Reciclap Backend
echo Iniciando el servidor de Reciclap...

:: Cambia al directorio donde está este .bat (debe ser la carpeta backend)
cd /d "%~dp0"

:: Activar el entorno virtual
call venv\Scripts\activate.bat

:: Iniciar el servidor con uvicorn
uvicorn app.interfaces.main:app --reload --host 127.0.0.1 --port 8000

:: Si ocurre un error o se cierra, pausa la ventana para ver el mensaje
pause