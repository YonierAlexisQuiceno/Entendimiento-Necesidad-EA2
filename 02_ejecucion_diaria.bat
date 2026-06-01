@echo off
echo ========================================================
echo   FASE 2: EJECUCION DIARIA DEL PROYECTO (EA1 y EA2)
echo ========================================================
echo.

REM Verificar si el entorno existe
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [ERROR] No se encontro el entorno virtual.
    echo Por favor, ejecuta primero '01_instalacion_inicial.bat'
    pause
    exit /b
)

REM Activar el entorno virtual
echo [*] Activando entorno virtual...
call venv\Scripts\activate

echo.
echo --- 1. Ejecutando Entrega 1 (Transaccional SQLite) ---
python src\ea1.py

echo.
echo --- 2. Ejecutando Entrega 2 (Scraper BBC - PostgreSQL) ---
python src\scraper.py

echo.
echo ========================================================
echo  PROCESO COMPLETADO EXITOSAMENTE
echo ========================================================
pause
