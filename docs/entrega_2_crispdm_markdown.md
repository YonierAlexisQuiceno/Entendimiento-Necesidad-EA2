# S30 - Entrega 2: Entendimiento de la Necesidad EA2

**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Programa:** Ingeniería de Software y Datos  
**Grupo:** PREICA2601B020089 - Programación para Análisis de Datos  
**Docente:** Ana Maria Lopez / Darkanita  
**Fecha:** 15 de Mayo de 2026

---

# 1. Actualización de la Necesidad y Contexto (Fase 1: Comprensión del Negocio)

## 1.1 Contexto Actualizado: ShopAnalytics S.A.S.

En la primera entrega (Fases 1 y 2 de CRISP-DM), se definió la necesidad de la empresa **ShopAnalytics S.A.S.** de optimizar su inventario mediante el análisis de datos transaccionales. Sin embargo, tras una revisión gerencial, se determinó que los factores externos (macroeconómicos, sociopolíticos y ambientales de Latinoamérica) tienen un impacto directo y profundo en la cadena de suministro, los tiempos de entrega y el comportamiento de compra de los clientes.

Por lo tanto, la necesidad del negocio evoluciona: **ShopAnalytics S.A.S.** requiere implementar un **Sistema de Inteligencia de Mercado**. El objetivo principal es extraer de forma automatizada, estructurada y recurrente, noticias relevantes del portal BBC Mundo Latinoamérica. Esta información servirá como base de conocimiento no estructurada para, en fases posteriores, entrenar modelos predictivos y de clasificación que emitan alertas tempranas sobre el inventario.

## 1.2 Objetivos del Web Scraping

- **Extraer:** Título, descripción, fecha, contenido completo y etiquetas (temas) de los artículos publicados en la sección de Latinoamérica de BBC Mundo.
- **Procesar:** Limpiar el HTML, eliminando ruido (anuncios, menús) y estructurando el texto para su futuro análisis de Procesamiento de Lenguaje Natural (NLP).
- **Ingestar:** Almacenar de forma segura y sin duplicados estos datos en una base de datos relacional robusta (PostgreSQL).
- **Integrar:** Preparar la arquitectura para que los datos sean visualizados en Power BI y procesados por un modelo de Machine Learning (SVM).

---

# 2. Comprensión y Preparación de los Datos (Fases 2 y 3 CRISP-DM)

## 2.1 Selección y Justificación de la Herramienta

Para este proyecto se evaluaron tres herramientas: **Scrapy**, **Selenium** y **BeautifulSoup**. La herramienta seleccionada fue **BeautifulSoup (BS4)** en combinación con **Requests**.

### Justificación Técnica

#### Naturaleza de la Fuente

Tras inspeccionar el DOM de:

```text
https://www.bbc.com/mundo/topics/c7zp57yyz25t
```

Se comprobó que el contenido principal de las noticias se carga en el HTML estático inicial. No es estrictamente necesario ejecutar JavaScript en un navegador completo.

#### Rendimiento y Eficiencia

BeautifulSoup extrae la información en fracciones de segundo y consume mínimos recursos de CPU y RAM. Esto contrasta con Selenium, que requiere levantar un WebDriver completo, haciendo el proceso hasta 3 veces más lento y costoso a nivel computacional.

#### Despliegue Cloud (Google Antigravity / Cloud Run)

Al ejecutarse como un script Python nativo en entorno local, `requests` y `bs4` consumen mínimos recursos del sistema. Esto facilita también su eventual despliegue en servicios serverless como Google Cloud Run sin dependencias pesadas.

## 2.2 Diseño del Scraper (Programación Orientada a Objetos - POO)

Para cumplir con los estándares de Ingeniería de Software y facilitar la mantenibilidad, el scraper se desarrolló bajo el paradigma de **Programación Orientada a Objetos**.

Se diseñó la clase `BBCMundoScraperPOO`, la cual encapsula:

### Atributos

- URLs base.
- Headers (`User-Agent`) para evasión de bloqueos.
- Motor de conexión a la base de datos (`SQLAlchemy engine`).

### Métodos de Extracción

- `obtener_sopa()`: Gestiona las peticiones HTTP con manejo de timeouts.
- `extraer_listado_noticias()`: Identifica las tarjetas de noticias mediante los atributos `data-testid="promo"`.
- `extraer_cuerpo_articulo()`: Navega iterativamente a cada URL extraída para recolectar el texto completo de los bloques `data-component="text-block"`.

### Manejo de Obstáculos

Se implementaron pausas éticas (`time.sleep`) para evitar bloqueos por **Rate Limiting** (Error HTTP 429) y se configuró un `User-Agent` que emula a Google Chrome de escritorio para evadir restricciones de seguridad (Error HTTP 403).

---

# 3. Modelado e Ingesta de Datos (Fase 4 CRISP-DM)

## 3.1 Arquitectura de la Base de Datos (PostgreSQL)

El script se conectó a una base de datos PostgreSQL mediante el ORM **SQLAlchemy** y el adaptador **psycopg2**. La elección de PostgreSQL se basa en su capacidad para manejar grandes volúmenes de texto (tipo `TEXT`) y su integración nativa con herramientas de visualización como Power BI.

### Estructura de la Tabla `noticias_mercado`

| Campo | Tipo |
|---|---|
| id | Serial, PK |
| titulo | VARCHAR |
| descripcion | TEXT |
| fecha_publicacion | VARCHAR |
| texto_completo | TEXT |
| temas_relacionados | VARCHAR |
| url | VARCHAR, UNIQUE |

> `texto_completo` es el campo clave para el modelo SVM.

## 3.2 Lógica de Ingesta y Prevención de Duplicados

Para asegurar la calidad de los datos, el método `guardar_en_postgres()` implementa una validación tipo **Upsert** o filtrado previo:

1. El script extrae las URLs de las noticias recién escrapeadas.
2. Consulta la tabla `noticias_mercado` en PostgreSQL para obtener las URLs ya existentes.
3. Se realiza una diferencia de conjuntos utilizando Pandas:

```python
df[~df['url'].isin(urls_existentes)]
```

4. Solo se ingieren (`df.to_sql(if_exists='append')`) los registros completamente nuevos, asegurando que ejecuciones diarias del script no generen redundancia.

---

# 4. Pruebas, Validación y Documentación de Errores

Durante el desarrollo se realizaron diversas pruebas unitarias y de integración:

## Prueba de Extracción (Parsing)

Se verificó que los selectores CSS extrajeran correctamente el contenido.

**Problema detectado:** Algunos artículos de video no contenían bloques de texto estándar.  
**Solución:** Se implementó un bloque `try-except` con condicionales para buscar la etiqueta `<main>` o `<article>` como método fallback.

## Prueba de Conexión a Base de Datos

Se forzó un error de credenciales para verificar la robustez del código.

**Solución:** Implementación de variables de entorno (`.env`) para ocultar contraseñas y uso de manejadores de excepciones de SQLAlchemy.

## Prueba de Duplicidad

Se ejecutó el scraper dos veces consecutivas.

- En la primera ejecución se insertaron 10 registros.
- En la segunda, el log de consola confirmó:

```text
"Limpieza de duplicados: 10 registros ignorados. 0 nuevos registros insertados"
```

Esto validó exitosamente la lógica de integridad.

---

# 5. Integración, CI/CD, Visualización y Despliegue (Google Antigravity)

Para escalar esta solución desde un entorno local hacia un sistema empresarial, se estructuró el repositorio local con los siguientes componentes de integración:

## 5.1 Estructura del Repositorio Local (Git)

El proyecto se versiona localmente y se enlaza a GitHub con la siguiente estructura:

```text
/src/scraper.py             # Código principal del scraper (POO)
/src/ingest_kaggle.py       # Ingesta de datos reales (Kaggle/Olist)
/docs/                      # Documentación (Markdown y Notebooks)
/data/                      # Archivos CSV de origen
/.env                       # Variables de entorno (Credenciales PostgreSQL)
/requirements.txt           # Dependencias
/.github/workflows/main.yml # Pipeline CI/CD
```

### Dependencias Principales

- pandas
- beautifulsoup4
- SQLAlchemy
- psycopg2-binary

## 5.2 CI/CD con GitHub Actions

Se configuró un flujo de trabajo (**Workflow**) en GitHub Actions. Al realizar un `git push` a la rama `main`, se dispara un webhook interno que valida que el código Python cumple con los estándares **PEP-8** y verifica que el archivo de dependencias esté actualizado.

## 5.3 Despliegue en GCP (Google Antigravity / Cloud Run)

El proyecto se ejecuta en un entorno local y puede ser desplegado de forma ágil hacia Google Cloud Run utilizando la plataforma como servicio, sin gestionar servidores. Esto permite configurar un desencadenador (**Cloud Scheduler**) que ejecute el scraper de forma autónoma todos los días a las 6:00 AM, poblando la base de datos PostgreSQL alojada en **Cloud SQL**.

## 5.4 Ingesta de Datos Transaccionales Reales (Kaggle)

Para simular un entorno de producción realista para ShopAnalytics, se creó el script `src/ingest_kaggle.py`, el cual lee los datasets de comercio electrónico de Olist (Kaggle) desde la carpeta `data/` y los ingesta masivamente en PostgreSQL usando Pandas y SQLAlchemy. Estos datos reales permitirán un cruce analítico fidedigno con las noticias extraídas.

## 5.5 Visualización en Power BI y Modelos SVM

Una vez los datos fluyen de forma constante hacia PostgreSQL:

### Power BI

Se conectará vía **DirectQuery** a PostgreSQL. Se desarrollará un Dashboard que muestre la frecuencia de noticias por país (usando la columna `temas_relacionados`) y la asocie con las métricas de ventas de **ShopAnalytics S.A.S.**

### Machine Learning (SVM)

El campo `texto_completo` será tokenizado y vectorizado mediante **TF-IDF**.

Posteriormente, un algoritmo de **Support Vector Machines (SVM)** clasificará la noticia en categorías de riesgo logístico, por ejemplo:

- Riesgo de Transporte
- Riesgo Cambiario
- Normal

Esto automatizará completamente la inteligencia de mercado de la compañía.

---

# Conclusión

Se logró implementar exitosamente la fase de preparación e ingesta de datos de la metodología **CRISP-DM**, superando los requerimientos mediante el uso de:

- Programación Orientada a Objetos.
- Bases de datos relacionales robustas (PostgreSQL).
- Arquitectura preparada para MLOps y Cloud Computing.

El proyecto quedó listo para futuras etapas de análisis avanzado, visualización y automatización mediante modelos de Machine Learning.

