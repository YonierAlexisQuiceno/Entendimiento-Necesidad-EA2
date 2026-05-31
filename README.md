# ShopAnalytics S.A.S. - Sistema de Inteligencia y Optimización de Inventario

**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Programa:** Ingeniería de Software y Datos  
**Curso:** Programación para Análisis de Datos  
**Docente:** Ana Maria Lopez  

---

## 1. Descripción del Proyecto

Este repositorio unifica y documenta el desarrollo analítico del **Sistema de Inteligencia de Mercado y Optimización de Inventario** para la empresa **ShopAnalytics S.A.S.**, implementado bajo el marco metodológico de **CRISP-DM**.

El sistema integra dos enfoques analíticos complementarios:
1. **Analítica Transaccional Local (Entrega 1 - EA1):** Simulación algorítmica de más de 5,000 registros transaccionales en Colombia persistidos en una base de datos local **SQLite** con indicadores medibles (KPIs) e inventario activo (`stock_actual` y `punto_reorden`). Cuenta con rutinas automáticas de validación de calidad de datos.
2. **Inteligencia de Mercado Web Scraping (Entrega 2 - EA2):** Extracción automatizada y estructurada mediante un Scraper en Programación Orientada a Objetos (POO) usando **BeautifulSoup** y **Requests** del portal **BBC Mundo Latinoamérica**. El scraper filtra duplicidades en caliente e ingesta la información en una base de datos relacional robusta **PostgreSQL** para análisis macroambientales de riesgo.

---

## 2. Estructura del Repositorio

```text
/
├── src/
│   ├── ea1.py            # Pipeline Analítico y Carga Transaccional (SQLite) - EA1
│   ├── scraper.py        # Scraper POO (BeautifulSoup) de BBC Mundo (PostgreSQL) - EA2
│   ├── ingest_kaggle.py  # Ingesta Olist (Kaggle) → PostgreSQL - EA2
│   └── create_db.py      # Script de verificación y creación de BD PostgreSQL
├── docs/
│   ├── entrega_1_crispdm_markdown.md    # Documentación Metodológica CRISP-DM EA1 (KPIs, SQLite)
│   ├── entrega_2_crispdm_markdown.md    # Documentación Metodológica CRISP-DM EA2 (Web Scraping, PostgreSQL)
│   ├── Quiceno_Rodriguez_Yonier_Alexis_Entendimiento_Necesidad_EA1_Mejorado.ipynb # Notebook Jupyter EA1
│   └── Scraper_POO_con_PostgreSQL.ipynb # Notebook Jupyter Scraper EA2
├── data/                 # Carpeta contenedora de datasets CSV reales
├── requirements.txt      # Dependencias empaquetadas del proyecto
├── run.bat               # Ejecutor automatizado secuencial para Windows
└── .env                  # Variables de entorno de conexión segura a base de datos
```

---

## 3. Requisitos de Ejecución

* **Lenguaje:** Python 3.10.x
* **Bases de Datos:**
  * **SQLite3** (Nativo en Python, no requiere instalación).
  * **PostgreSQL** local o cloud (puerto `5432`, base de datos `shopanalytics` creada, credenciales especificadas en `.env`).

---

## 4. Guía de Ejecución Rápida

### Opción A: Ejecución Automatizada (Recomendada en Windows)
Haz doble clic sobre el ejecutable `run.bat` o ejecútalo desde la consola:
```powershell
.\run.bat
```
Este script instalará las dependencias en `requirements.txt` y correrá secuencialmente la ingesta y el web scraper de noticias.

### Opción B: Ejecución Manual por Entregas

#### Ejecutar Entrega 1 (SQLite y KPIs de Inventario):
```bash
python src/ea1.py
```
* **Qué hace:** Genera 5,000 transacciones, las ingesta en `shopanalytics.db`, ejecuta rutinas automáticas de calidad (PK únicas, consistencia referencial, cero huérfanos) e imprime 4 reportes analíticos de reabastecimiento, sobrestock, rotación y regiones.

#### Ejecutar Entrega 2 (Scraper de Noticias y PostgreSQL):
```bash
python src/scraper.py
```
* **Qué hace:** Escanea la sección de Latinoamérica de BBC Mundo, extrae título, descripción, fecha, texto plano y temas relacionados para cada noticia, limpia duplicados en caliente e inserta la información en la tabla `noticias_mercado` de PostgreSQL.

---

## 5. Control de Calidad e Integridad de Datos

* **Entrega 1:** Integración de pruebas automáticas en `ea1.py` que comprueban que no existen registros duplicados en llaves primarias ni llaves foráneas huérfanas en la base de datosSQLite.
* **Entrega 2:** Inserción inteligente en `scraper.py` que compara las URLs escrapeadas en memoria con las de la tabla `noticias_mercado` de PostgreSQL para filtrar repetidos en caliente.

---

## 6. Variables de Entorno (`.env`)
Configura un archivo `.env` en la raíz del proyecto con tus credenciales de PostgreSQL:
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=shopanalytics
DB_USER=postgres
DB_PASSWORD=12345
```
