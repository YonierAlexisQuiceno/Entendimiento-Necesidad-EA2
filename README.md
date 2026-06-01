# ShopAnalytics S.A.S. - Sistema de Inteligencia y Optimización de Inventario

**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Programa:** Ingeniería de Software y Datos  
**Curso:** Programación para Análisis de Datos  
**Docente:** Ana Maria Lopez  

---

## 1. Descripción del Proyecto

Este repositorio unifica y documenta el desarrollo analítico del **Sistema de Inteligencia de Mercado y Optimización de Inventario** para la empresa **ShopAnalytics S.A.S.**, implementado bajo el marco metodológico de **CRISP-DM**.

El sistema integra tres enfoques analíticos complementarios:
1. **Analítica Transaccional Local (EA1):** Simulación algorítmica de más de 5,000 registros transaccionales persistidos en **SQLite** con KPIs de inventario activo (`stock_actual` y `punto_reorden`).
2. **Inteligencia de Mercado vía Web Scraping (EA2):** Extracción automatizada mediante un Scrapper POO usando **BeautifulSoup** desde múltiples secciones de **BBC Mundo** (Economía, Tecnología, Internacional), con ingesta en **PostgreSQL**.
3. **Transformación y Enriquecimiento NLP (EA3):** Modelo de Procesamiento de Lenguaje Natural basado en reglas que clasifica cada noticia por nivel de riesgo (Alto, Medio, Bajo) y categoría (Geopolítico, Operativo, Financiero), con visualización en **Power BI** vía DirectQuery.

---

## 2. Estructura del Repositorio

```text
/
├── src/
│   ├── ea1.py            # Pipeline Analítico y Carga Transaccional (SQLite) - EA1
│   ├── scrapper.py       # Scrapper POO (BeautifulSoup) de BBC Mundo (PostgreSQL) - EA2
│   ├── modelo.py         # Modelo NLP de enriquecimiento y clasificación de riesgo - EA3
│   ├── ejecucion.py      # Orquestador del pipeline (Scrapper + NLP + Auditoría) - EA3
│   ├── ingest_kaggle.py  # Ingesta Olist (Kaggle) → PostgreSQL
│   └── create_db.py      # Verificación y creación de BD PostgreSQL
├── docs/
│   ├── entrega_1_crispdm_markdown.md     # Documentación CRISP-DM EA1
│   ├── entrega_2_crispdm_markdown.md     # Documentación CRISP-DM EA2
│   ├── Quiceno_Rodriguez_Yonier_Alexis_EA3.md  # Informe EA3 (Enriquecimiento + Power BI)
│   ├── Quiceno_Rodriguez_Yonier_Alexis_EA4.md  # Informe EA4 (Video + CI/CD)
│   └── guia_powerbi_ea3.md              # Guía de conexión PostgreSQL → Power BI
├── .github/workflows/ci.yml  # Pipeline de Integración Continua (GitHub Actions)
├── 01_instalacion_inicial.bat # Instalación y configuración inicial
├── 02_ejecucion_diaria.bat    # Ejecución completa del proyecto
├── requirements.txt           # Dependencias del proyecto
└── .env                       # Variables de entorno (NO subir a Git)
```

---

## 3. Requisitos de Ejecución

* **Lenguaje:** Python 3.10+
* **Bases de Datos:**
  * **SQLite3** (Nativo en Python, no requiere instalación).
  * **PostgreSQL** local (puerto `5432`, base de datos `shopanalytics`).

---

## 4. Guía de Ejecución Rápida

### Primera vez (Instalación)
```powershell
.\01_instalacion_inicial.bat
```
Crea el entorno virtual, instala dependencias, crea la BD en PostgreSQL e ingesta datos de Kaggle.

### Ejecución del proyecto
```powershell
.\02_ejecucion_diaria.bat
```
Ejecuta secuencialmente: EA1 (SQLite) → EA2 (Scrapper BBC) → EA3 (NLP + Enriquecimiento).

### Ejecución Manual por Entregas
```bash
# Activar entorno virtual
.\venv\Scripts\activate

# EA1 - Transaccional SQLite
python src/ea1.py

# EA2 - Scrapper BBC Mundo
python src/scrapper.py

# EA3 - Pipeline completo (Scrapper + Modelo NLP + Auditoría)
python src/ejecucion.py
```

---

## 5. Variables de Entorno (`.env`)
Configura un archivo `.env` en la raíz del proyecto:
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=shopanalytics
DB_USER=postgres
DB_PASSWORD=tu_contraseña
```
