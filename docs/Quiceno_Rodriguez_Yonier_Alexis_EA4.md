# EA4 - Video Sustentación, Control de Versiones e Integración Continua

**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Materia:** Programación para Análisis de Datos  
**Fecha:** 7 de junio de 2026  

---

## 1. Introducción
Este documento corresponde a la cuarta y última entrega (EA4) del proyecto **ShopAnalytics S.A.S.**. En esta fase culminante se presenta la consolidación total del proyecto a través de un video de sustentación técnica. Adicionalmente, como valor agregado y muestra de profesionalismo en Ingeniería de Software, se han integrado metodologías ágiles de control de versiones y DevOps (CI/CD).

## 2. Descripción del Problema y Solución Propuesta
El principal problema abordado a lo largo del curso fue el **sobrestock y el quiebre de inventario** debido a la falta de trazabilidad de los datos históricos y a la ceguera frente a riesgos externos (inflación, huelgas, cierres de fronteras).

**La solución desplegada constó de:**
1.  Un pipeline transaccional (SQLite) y masivo (PostgreSQL).
2.  Un Web Scraper orientado a objetos para inteligencia de mercado.
3.  Un modelo de Enriquecimiento NLP que categoriza el riesgo logístico.
4.  Un tablero automatizado en Power BI para la gerencia.

## 3. Integración Continua y Control de Versiones (Valor Extra)
Para garantizar la estabilidad del software y prepararlo para un entorno corporativo real, se implementaron las siguientes tecnologías:

*   **Git y Control de Versiones:** Todo el código fuente está versionado bajo un repositorio Git local con flujo estructurado en tres ramas: `dev` (desarrollo), `qa` (pruebas de calidad) y `main` (producción). Se cuenta con un archivo `.gitignore` profesional para excluir dependencias y credenciales (`.env`).
*   **Pruebas Automatizadas (pytest):** Se implementaron pruebas unitarias en `tests/test_pipeline.py` para verificar que la lógica fundamental de calidad y procesamiento de datos del pipeline se cumpla con cada cambio de código.
*   **Integración Continua (CI - GitHub Actions):** Se configuró `.github/workflows/ci.yml` para dispararse en cada Pull Request hacia `dev`, `qa` o `main`, ejecutando de forma automatizada:
    *   Instalación de dependencias y linting con `flake8`.
    *   Validación de la compilación y sintaxis de todos los scripts principales (`ea1.py`, `scrapper.py`, `modelo.py`, `ejecucion.py`, `pipeline.py`, `dashboard.py`).
    *   Ejecución de pruebas unitarias (`pytest`).
*   **Despliegue Continuo (CD - GitHub Actions):** Se configuró `.github/workflows/cd.yml` para dispararse en cada push a las ramas del flujo, orquestando el pipeline según el ambiente:
    *   **dev / qa:** Ejecución y generación de reportes simulados en entornos de pre-producción.
    *   **main (production):** Ejecución total del ETL en DuckDB, generación del dashboard interactivo en `output/index.html` y publicación directa en **GitHub Pages** mediante despliegue nativo de Actions (sin requerir ramas intermedias).
*   **Documentación de Configuración Manual:** Se ha actualizado la guía exhaustiva ([guia_configuracion_manual.md](guia_configuracion_manual.md)) detallando los pasos manuales en el portal de GitHub para activar Pages, crear entornos y configurar protecciones de rama.

## 4. Enlace al Video de Sustentación
*(Pegar aquí el link de YouTube o Google Drive con el video grabado).*
*   **Enlace:** `[AQUÍ TU ENLACE AL VIDEO]`

El video abarca:
1.  **Contexto del negocio:** La problemática y la metodología CRISP-DM.
2.  **Demostración de Código:** Explicación del orquestador, el scraper y el modelo de NLP.
3.  **Ejecución en Vivo:** Ejecución del pipeline con ingesta hacia PostgreSQL.
4.  **Tablero Power BI:** Análisis en tiempo real de los datos enriquecidos.
5.  **Buenas Prácticas:** Muestra del archivo YAML de GitHub Actions.

## 5. Resultados Globales y Conclusiones
*   La metodología CRISP-DM demostró ser un marco de trabajo excepcionalmente robusto, permitiendo escalar un simple análisis exploratorio hasta una arquitectura de datos corporativa.
*   El cruce de análisis de inventario interno con alertas macroeconómicas procesadas con NLP provee una ventaja competitiva fundamental frente a modelos predictivos tradicionales.
*   El uso de herramientas como Python, PostgreSQL, Power BI, Git y GitHub Actions ratifican que el perfil de Análisis de Datos no se limita a hacer reportes, sino a desarrollar software inteligente y escalable.

## 6. Bibliografía
* McKinney, W. (2012). *Python for data analysis*. O'Reilly Media, Inc.
* Chacon, S., & Straub, B. (2014). *Pro Git*. Apress.
* Wirth, R., & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining.


## Referencias

* Wirth, R., & Hipp, J. (2000). *CRISP-DM: Towards a standard process model for data mining*. Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining.
* McKinney, W. (2012). *Python for Data Analysis*. O'Reilly Media.
* Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media.
* Olist. (2018). *Brazilian E-Commerce Public Dataset by Olist*. Kaggle. Recuperado de https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
* BBC Mundo. (2024). *BBC News Mundo*. Recuperado de https://www.bbc.com/mundo
* Python Software Foundation. (2024). *SQLAlchemy Documentation*. Recuperado de https://docs.sqlalchemy.org/
