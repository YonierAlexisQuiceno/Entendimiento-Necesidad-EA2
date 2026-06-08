@echo off
:: UT-8 encoding para caracteres en español
chcp 65001 > nul
title ShopAnalytics S.A.S. - Consola de Control de Entregas
color 0B

:MENU
cls
echo =======================================================================
echo          SHOPANALYTICS S.A.S. - CONSOLA DE CONTROL DE ENTREGAS
echo =======================================================================
echo.
echo [1] Configurar Entorno e Instalar Dependencias (venv)
echo [2] Verificar/Crear Base de Datos PostgreSQL (create_db.py)
echo [3] Ingestar Datos Iniciales de Kaggle (ingest_kaggle.py)
echo [4] Ejecutar EA1: Analítica Transaccional (ea1.py - SQLite)
echo [5] Ejecutar EA2: Web Scraping de BBC Mundo (scrapper.py)
echo [6] Ejecutar EA3: Pipeline NLP + Auditoría (ejecucion.py - PostgreSQL)
echo [7] Ejecutar EA4: Pipeline Medallion con DuckDB (pipeline.py)
echo [8] Lanzar Servidor del Dashboard Local (app.py)
echo [9] Ejecutar Pruebas Unitarias del Proyecto (pytest)
echo [10] Salir
echo.
echo =======================================================================
set /p op=Seleccione una opción [1-10]: 

if "%op%"=="1" goto OP1
if "%op%"=="2" goto OP2
if "%op%"=="3" goto OP3
if "%op%"=="4" goto OP4
if "%op%"=="5" goto OP5
if "%op%"=="6" goto OP6
if "%op%"=="7" goto OP7
if "%op%"=="8" goto OP8
if "%op%"=="9" goto OP9
if "%op%"=="10" goto EXIT
goto MENU

:OP1
echo.
echo === CONFIGURANDO ENTORNO VIRTUAL ===
if not exist venv (
    echo Creando entorno virtual venv...
    python -m venv venv
)
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo Instalando dependencias de requirements.txt...
pip install -r requirements.txt
echo.
echo [OK] Entorno configurado correctamente.
pause
goto MENU

:OP2
echo.
echo === VERIFICANDO BASE DE DATOS POSTGRESQL ===
call venv\Scripts\activate.bat
python src/create_db.py
pause
goto MENU

:OP3
echo.
echo === INGESTANDO DATOS DESDE KAGGLE A POSTGRESQL ===
call venv\Scripts\activate.bat
python src/ingest_kaggle.py
pause
goto MENU

:OP4
echo.
echo === EJECUTANDO EA1: ANALÍTICA TRANSACCIONAL ===
call venv\Scripts\activate.bat
python src/ea1.py
pause
goto MENU

:OP5
echo.
echo === EJECUTANDO EA2: WEB SCRAPING BBC MUNDO ===
call venv\Scripts\activate.bat
python src/scrapper.py
pause
goto MENU

:OP6
echo.
echo === EJECUTANDO EA3: PIPELINE NLP + ENRIQUECIMIENTO ===
call venv\Scripts\activate.bat
python src/ejecucion.py
pause
goto MENU

:OP7
echo.
echo === EJECUTANDO EA4: PIPELINE MEDALLION DUCKDB ===
call venv\Scripts\activate.bat
python src/pipeline.py
pause
goto MENU

:OP8
echo.
echo === LEVANTANDO SERVIDOR DASHBOARD (FLASK/PLOTLY) ===
call venv\Scripts\activate.bat
echo El servidor se iniciará en: http://localhost:5000
python src/app.py
pause
goto MENU

:OP9
echo.
echo === EJECUTANDO PRUEBAS UNITARIAS ===
call venv\Scripts\activate.bat
pytest tests/ -v
pause
goto MENU

:EXIT
echo.
echo ¡Hasta luego! Gracias por usar la Consola de Control de ShopAnalytics.
timeout /t 2 > nul
exit
