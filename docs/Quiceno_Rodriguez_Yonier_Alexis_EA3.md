# EA3 - Transformación, Enriquecimiento y Análisis en Power BI

**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Materia:** Programación para Análisis de Datos  
**Fecha:** 31 de mayo de 2026  

---

## 1. Introducción
Este documento detalla la tercera entrega (EA3) del proyecto **ShopAnalytics S.A.S.**. En esta fase, el objetivo principal fue tomar los datos crudos obtenidos del scraping, enriquecerlos utilizando técnicas avanzadas de Procesamiento de Lenguaje Natural (NLP) y visualizarlos en Power BI. Esta transformación eleva la madurez del proyecto de una simple "base de datos transaccional" a un "Sistema de Inteligencia de Mercado y Alertas Tempranas".

## 2. Descripción del Problema
ShopAnalytics enfrenta el desafío de no poder prever retrasos en su cadena de suministro. Las noticias extraídas (desde BBC Mundo) contenían un gran valor contextual sobre economía mundial, tecnología y relaciones internacionales, pero en formato de texto no estructurado. Un equipo directivo no tiene el tiempo ni los recursos para leer y evaluar el riesgo de cientos de noticias diarias antes de aprobar una compra internacional.

## 3. Objetivos
* Escalar el volumen de datos escrapeando múltiples secciones clave de BBC Mundo (Economía, Tecnología, Internacional).
* Transformar el texto extraído aplicando un modelo de limpieza y análisis semántico basado en reglas.
* Asignar un **Nivel de Riesgo Logístico** cuantitativo y una **Categoría de Riesgo Dominante** (Operativo, Financiero, Geopolítico) a cada artículo.
* Consolidar los datos enriquecidos en una base de datos PostgreSQL.
* Diseñar un tablero analítico en Power BI mediante DirectQuery.

## 4. Descripción de los Datos Disponibles
Contamos con una arquitectura de datos híbrida en PostgreSQL:
*   Datos históricos transaccionales (simulación de Olist).
*   La tabla `noticias_mercado`, alimentada por el scraper. Incluye `titulo`, `descripcion`, `fecha`, y `texto_completo`.

## 5. Solución Propuesta (Transformación y Enriquecimiento)
Se implementaron dos mejoras estructurales:
1.  **Escalabilidad del Scrapper (`scrapper.py`):** Se modificó la arquitectura POO para iterar sobre un arreglo de múltiples URLs, aumentando drásticamente la variedad de la muestra.
2.  **Modelo NLP (`modelo.py`):**
    *   Lee los registros masivos desde PostgreSQL.
    *   Ejecuta la función `aplicar_nlp_basico`, que cuenta la densidad léxica de tres diccionarios especializados: Geopolítico (ej. *sanciones, guerra*), Operativo (ej. *huelga, clima*) y Financiero (ej. *inflación, aranceles*).
    *   Dependiendo del peso ponderado, el algoritmo determina la categoría dominante y el nivel de gravedad.
    *   Genera una nueva tabla `noticias_enriquecidas` y despliega la Vista SQL `vw_riesgo_logistico`, lista para su consumo visual.

## 6. Metodología CRISP-DM
* **Fase 3 (Preparación de los Datos):** Se aplicaron técnicas de *lower-casing*, limpieza de caracteres especiales y tokenización.
* **Fase 4 (Modelado):** Aplicación del modelo de inferencia multicategoría.
* **Fase 5 (Evaluación):** Validación en consola de la matriz de riesgos.
* **Fase 6 (Despliegue):** Integración continua en la base de datos y consumo visual mediante Power BI en tiempo real.

## 7. Análisis de Datos Enriquecidos y Power BI
Se conectó exitosamente PostgreSQL con Power BI Desktop utilizando ODBC (DirectQuery), lo que asegura que el modelo de datos de Power BI sea siempre un reflejo instantáneo de la base de datos física.

*El tablero de Power BI permite analizar:*
1. **Distribución Categórica:** Un gráfico circular que expone si el riesgo actual del mercado es principalmente Geopolítico, Financiero u Operativo.
2. **Volumen de Alertas (Gravedad):** Gráfico de barras que alerta sobre cuántas noticias clasifican como "Riesgo Alto" hoy.
3. **KPI de Score de Riesgo Global:** Un semáforo cuantitativo que le dice a la gerencia el estado actual del comercio exterior.

*(Nota: Se anexa el archivo `.pbix` junto con esta entrega, el cual contiene el tablero operativo).*

## 8. Resultados y Conclusiones
* El enriquecimiento de datos comprobó su valía al transformar un repositorio de texto muerto en un panel dinámico de toma de decisiones.
* La categorización de los riesgos permite a los gerentes de compras derivar los problemas al departamento correcto (e.g., derivar alertas financieras al equipo de tesorería).
* La automatización completa del pipeline (Scraping -> NLP -> PostgreSQL -> Power BI) ahorra costos operativos, mitigando pérdidas por demoras en aduanas.

## 9. Bibliografía
* McKinney, W. (2012). *Python for data analysis*. O'Reilly Media, Inc.
* Microsoft. (2023). *Conectar PostgreSQL a Power BI*. Documentación oficial.
* Wirth, R., & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining.


## Referencias

* Wirth, R., & Hipp, J. (2000). *CRISP-DM: Towards a standard process model for data mining*. Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining.
* McKinney, W. (2012). *Python for Data Analysis*. O'Reilly Media.
* Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media.
* Olist. (2018). *Brazilian E-Commerce Public Dataset by Olist*. Kaggle. Recuperado de https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
* BBC Mundo. (2024). *BBC News Mundo*. Recuperado de https://www.bbc.com/mundo
* Python Software Foundation. (2024). *SQLAlchemy Documentation*. Recuperado de https://docs.sqlalchemy.org/
