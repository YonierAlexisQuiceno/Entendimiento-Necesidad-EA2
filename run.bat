@echo off
set PY_PATH=%LOCALAPPDATA%\Programs\Python\Python310\python.exe

echo --- 1. Instalando Dependencias en Python 3.10 ---
%PY_PATH% -m pip install -r requirements.txt

echo.
echo --- 2. Ingestando Datos de Kaggle ---
%PY_PATH% src\ingest_kaggle.py

echo.
echo --- 3. Ejecutando Scraper BBC ---
%PY_PATH% src\scraper.py

echo.
echo =========================================
echo  PROCESO COMPLETADO EXITOSAMENTE
echo =========================================
pause
