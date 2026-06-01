@echo off
echo ========================================================
echo   LEVANTANDO DASHBOARD WEB DE SHOPANALYTICS S.A.S.
echo ========================================================
echo.

REM Activar el entorno virtual
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [ERROR] No se encontro el entorno virtual. Ejecuta 01_instalacion_inicial.bat primero.
    pause
    exit /b
)
call venv\Scripts\activate

REM Abrir el navegador en el puerto 5000 (esperamos 3 segundos para que inicie Flask)
echo [*] Abriendo el navegador web...
start "" "http://127.0.0.1:5000"

REM Ejecutar Flask
echo [*] Iniciando servidor backend Flask...
python src\app.py

pause
