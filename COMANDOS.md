# Guía de Ejecución Rápida y Comandos - ShopAnalytics S.A.S.

Esta guía consolidada contiene todos los comandos y ejecuciones necesarias para cada una de las entregas del proyecto (**EA1**, **EA2**, **EA3**, **EA4**), ideal para tener en una pantalla secundaria durante la grabación de tus videos explicativos o ejecución del proyecto.

> [!TIP]
> Puedes usar la consola interactiva ejecutando en tu terminal:
> ```powershell
> .\EJECUTAR_PROYECTO.bat
> ```

---

## 📋 Tabla de Contenidos de Ejecución

1. [Configuración Inicial](#1-configuracion-inicial)
2. [Entrega EA1: Analítica Transaccional (SQLite)](#2-entrega-ea1-analitica-transaccional-sqlite)
3. [Entrega EA2: Web Scraping (BBC Mundo & PostgreSQL)](#3-entrega-ea2-web-scraping-bbc-mundo--postgresql)
4. [Entrega EA3: Clasificación de Riesgo NLP & Power BI](#4-entrega-ea3-clasificacion-de-riesgo-nlp--power-bi)
5. [Entrega EA4: Arquitectura Medallion & CI/CD (DuckDB)](#5-entrega-ea4-arquitectura-medallion--cicd-duckdb)
6. [Pruebas y Verificación](#6-pruebas-y-verificacion)

---

## 1. Configuración Inicial

Antes de correr cualquier pipeline, prepara el entorno virtual y las dependencias:

```powershell
# 1. Crear el entorno virtual
python -m venv venv

# 2. Activar el entorno virtual
# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# En Windows (CMD):
.\venv\Scripts\activate.bat

# 3. Instalar dependencias requeridas
pip install -r requirements.txt

# 4. Crear la Base de Datos PostgreSQL
python src/create_db.py

# 5. Cargar datos transaccionales crudos (Olist/Kaggle) a PostgreSQL
python src/ingest_kaggle.py
```

---

## 2. Entrega EA1: Analítica Transaccional (SQLite)

Simulación del sistema transaccional local con persistencia en **SQLite3** y cálculo automático de métricas de inventario (`stock_actual` y `punto_reorden`).

```powershell
# Activar entorno virtual si no está activo
.\venv\Scripts\activate

# Ejecutar script EA1
python src/ea1.py
```
* **Resultado:** Crea la base de datos `shopanalytics.db` y genera un reporte en consola con la simulación de ventas y cálculo de stock de seguridad.

---

## 3. Entrega EA2: Web Scraping (BBC Mundo & PostgreSQL)

Extracción automatizada de noticias en secciones clave de **BBC Mundo** con control de duplicados e inserción estructurada en **PostgreSQL**.

```powershell
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar el Scrapper POO
python src/scrapper.py
```
* **Resultado:** Inserta los artículos extraídos directamente en la tabla `noticias` de la base de datos `shopanalytics` en PostgreSQL.

---

## 4. Entrega EA3: Clasificación de Riesgo NLP & Power BI

Enriquecimiento mediante un clasificador de reglas NLP que analiza el texto para determinar el nivel de riesgo de cadena de suministro (Alto, Medio, Bajo) y genera una bitácora de auditoría histórica.

```powershell
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar el Orquestador del Pipeline Completo (Scraper + Modelo NLP + Bitácora)
python src/ejecucion.py
```
* **Resultado:** Clasifica las noticias en PostgreSQL y actualiza/crea el archivo `auditoria.txt` en la raíz del proyecto.
* **Power BI:** Abre el reporte en Power BI y haz clic en **Actualizar** para ver los nuevos datos ingresados en tiempo real vía DirectQuery.

---

## 5. Entrega EA4: Arquitectura Medallion & CI/CD (DuckDB)

Pipeline analítico de alta velocidad operando en memoria con **DuckDB**, cargando desde un CSV de ventas y estructurando los datos en capas **Bronze**, **Silver** y **Gold**.

```powershell
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar Pipeline DuckDB (Medallion)
python src/pipeline.py

# Levantar el servidor web local para visualizar el dashboard interactivo
python src/app.py
```
* **Resultado:** 
  * Genera el archivo analítico consolidado en `output/gold.json`.
  * Levanta el backend local en `http://localhost:5000` para servir el dashboard interactivo de ventas.

---

## 6. Pruebas y Verificación

Para asegurar que todo el código cumple con los criterios de calidad y pasa las validaciones automáticas de Integración Continua (CI/CD):

```powershell
# Activar entorno virtual
.\venv\Scripts\activate

# Ejecutar la suite completa de pruebas unitarias
pytest tests/ -v
```
* **Resultado:** Ejecuta las pruebas automatizadas del pipeline analítico verificando la limpieza de datos y consistencia del modelo.
