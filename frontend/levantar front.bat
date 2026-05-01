@echo off
title Reciclap Frontend
echo ========================================
echo  Iniciando Frontend de Reciclap
echo ========================================
echo.

:: Cambia al directorio donde está este archivo .bat
cd /d "%~dp0"

echo Verificando Node.js...
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no esta instalado.
    echo Instala Node.js desde https://nodejs.org
    pause
    exit /b 1
)

echo Iniciando servidor en http://localhost:3000
echo Presiona Ctrl+C para detener.
echo.

:: Usa npx serve si está disponible, sino intenta con Python o muestra error
npx --version >nul 2>nul
if %errorlevel% equ 0 (
    npx serve . -l 3000 --no-clipboard
) else (
    echo npx no disponible. Intentando con Python...
    python --version >nul 2>nul
    if %errorlevel% equ 0 (
        python -m http.server 3000
    ) else (
        echo [ERROR] No se encontro ni npx ni Python.
        echo Instala Node.js o Python para ejecutar el servidor.
        pause
        exit /b 1
    )
)

pause