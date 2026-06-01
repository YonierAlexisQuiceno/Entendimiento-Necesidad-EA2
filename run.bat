@echo off
echo ========================================================
echo   CONFIGURACION Y EJECUCION DE SHOPANALYTICS S.A.S.
echo ========================================================
echo.

REM 1. Crear entorno virtual si no existe
IF NOT EXIST "venv\Scripts\python.exe" (
    echo [*] Creando entorno virtual venv ...
    python -m venv venv
) ELSE (
    echo [*] El entorno virtual ya existe.
)

REM 2. Activar el entorno virtual
echo [*] Activando entorno virtual...
call venv\Scripts\activate

REM 3. Instalar dependencias
echo.
echo --- 1. Instalando Dependencias en el Entorno Virtual ---
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo --- 2. Ejecutando Entrega 1 (Transaccional SQLite) ---
python src\ea1.py

echo.
echo --- 3. Ejecutando Entrega 2 (Scraper BBC - PostgreSQL) ---
python src\scraper.py

REM (Opcional) Si necesitas ejecutar la ingesta de Kaggle, descomenta la siguiente línea:
REM python src\ingest_kaggle.py

echo.
echo =========================================
echo  PROCESO COMPLETADO EXITOSAMENTE
echo =========================================
pause
