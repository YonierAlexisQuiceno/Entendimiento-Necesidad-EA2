# Portada
**Título:** Video Sustentación, Control de Versiones e Integración Continua (EA4)  
**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Programa:** Ingeniería de Software y Datos  
**Grupo:** PREICA2601B020089 - Programación para Análisis de Datos  
**Docente:** Ana Maria Lopez  
**Fecha:** 7 de junio de 2026  

---

## 1. Introducción
Este documento corresponde a la cuarta y última entrega (EA4) del proyecto **ShopAnalytics S.A.S.**. En esta fase culminante se presenta la consolidación total del proyecto a través de un video de sustentación técnica. Adicionalmente, como valor agregado y muestra de profesionalismo en Ingeniería de Software, se han integrado metodologías ágiles de control de versiones y DevOps (CI/CD).

## 2. Descripción del Problema
El principal problema abordado a lo largo del curso fue el **sobrestock y el quiebre de inventario** debido a la falta de trazabilidad de los datos históricos y a la ceguera frente a riesgos macroeconómicos externos (inflación, huelgas, cierres de fronteras).

## 3. Objetivos
* Explicar de manera concisa la solución implementada a través de un video estructurado.
* Garantizar la calidad del código mediante el versionamiento en Git.
* Automatizar las pruebas y el despliegue del proyecto implementando pipelines de Integración y Despliegue Continuo (CI/CD).

## 4. Descripción de los Datos Disponibles
Se consolidó una arquitectura de base de datos híbrida (SQLite para simulaciones locales y PostgreSQL para almacenamiento masivo), unificando datos transaccionales internos con noticias de mercado estructuradas mediante NLP.

## 5. Solución Propuesta (y Valor Extra CI/CD)
La solución desplegada consta de un pipeline transaccional, un Web Scraper orientado a objetos y un modelo de Enriquecimiento NLP. Como **Valor Extra** se implementó Integración y Despliegue Continuo:
* **Pruebas Automatizadas (pytest):** Se implementaron pruebas unitarias en `tests/test_pipeline.py`.
* **CI/CD (GitHub Actions):** Se configuraron los flujos `.github/workflows/ci.yml` y `cd.yml` para ejecutar pruebas, hacer linting y desplegar reportes automáticamente en GitHub Pages.

## 6. Metodología Empleada (CRISP-DM)
El proyecto entero encapsula las 6 fases: Entendimiento del Negocio, Comprensión de Datos, Preparación (Scraping/Limpieza), Modelado (NLP/PostgreSQL), Evaluación (Validaciones SQL/Pytest) y Despliegue (CI/CD, Power BI y GitHub Pages).

## 7. Análisis de Datos Enriquecidos
A través de Power BI, se demostró cómo la vectorización del texto crudo permitió alertar a la gerencia logística sobre focos de riesgo geopolítico y operativo de manera cuantitativa.

## 8. Conexión y Visualización en Power BI
La conexión DirectQuery con PostgreSQL sirvió como el frontend definitivo. Para más detalles técnicos, revisar la [Guía de Configuración Manual](guia_configuracion_manual.md) y el archivo `Quiceno_Rodriguez_Yonier_Alexis_EA3.pbix`.

## 9. Resultados y Conclusiones
* La metodología CRISP-DM demostró ser un marco de trabajo excepcionalmente robusto, permitiendo escalar un simple análisis exploratorio hasta una arquitectura corporativa.
* El uso de herramientas DevOps (GitHub Actions, Pytest) eleva la madurez del equipo de analítica hacia la Ingeniería de Datos pura.
* **Arquitectura Medallion:** Se comprobó la eficacia de procesar los datos en capas lógicas (Bronze, Silver, Gold), lo que permite separar responsabilidades, limpiar datos de forma estructurada y alimentar el Dashboard final directamente desde la capa Gold.
* **Responsabilidad y Etica en el uso de IA (Accountability):** A lo largo del desarrollo (ej. pipeline ETL con DuckDB, visualizaciones en Plotly, etc.), se empleó Inteligencia Artificial Generativa. Sin embargo, se tuvo pleno entendimiento de cada línea de código generada. La responsabilidad de garantizar que las decisiones analíticas sean correctas (por ejemplo, definir la normalización adecuada o evitar sesgos por muestras pequeñas en los gráficos) recae totalmente en el Ingeniero de Datos, no en la IA. La IA es un copiloto, pero el gobierno de la información y la asertividad del negocio es 100% humano.

## 10. Bibliografía
* Wirth, R., & Hipp, J. (2000). *CRISP-DM: Towards a standard process model for data mining*. Proceedings of the 4th International Conference on the Practical Applications of Knowledge Discovery and Data Mining.
* Chacon, S., & Straub, B. (2014). *Pro Git*. Apress.

---

## 11. Anexos
**A. Enlace al Video de Sustentación**
*   **Enlace YouTube:** [Ver Sustentación de ShopAnalytics S.A.S.](https://youtu.be/Sustentacion_EA4_ShopAnalytics)

El video abarca el contexto del negocio, la demostración del orquestador Python y el scraper, la ejecución en vivo del modelo NLP, el análisis dinámico en Power BI y la explicación de los pipelines automatizados (YAML) de GitHub Actions.
