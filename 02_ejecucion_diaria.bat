@echo off
echo ========================================================
echo   EJECUCION COMPLETA DEL PROYECTO (EA1, EA2 y EA3)
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
echo --- 2. Ejecutando Entrega 2 (Scrapper BBC - PostgreSQL) ---
python src\scrapper.py

echo.
echo --- 3. Ejecutando Entrega 3 (Modelo NLP y Enriquecimiento) ---
python src\ejecucion.py

echo.
echo ========================================================
echo  PROCESO COMPLETADO EXITOSAMENTE
echo ========================================================
pause
