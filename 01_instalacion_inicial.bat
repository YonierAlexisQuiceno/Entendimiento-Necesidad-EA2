@echo off
echo ========================================================
echo   FASE 1: INSTALACION Y CONFIGURACION INICIAL
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

REM 4. Creacion de la base de datos PostgreSQL
echo.
echo --- 2. Creando y validando Base de Datos PostgreSQL ---
python src\create_db.py

REM 5. Ingesta Inicial de Kaggle
echo.
echo --- 3. Ingestando Datos Historicos de Kaggle (Olist) ---
python src\ingest_kaggle.py

echo.
echo ========================================================
echo  INSTALACION Y CONFIGURACION COMPLETADA EXITOSAMENTE
echo ========================================================
pause
