# EA3 - Transformación, Enriquecimiento y Análisis en Power BI

**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Materia:** Programación para Análisis de Datos  
**Fecha:** 31 de mayo de 2026  

---

## 1. Introducción
Este documento detalla la tercera entrega (EA3) del proyecto **ShopAnalytics S.A.S.**. En las entregas anteriores, construimos un modelo relacional y un scraper orientado a objetos para extraer noticias sobre logística y economía. En esta fase, el objetivo principal es tomar esos datos crudos, enriquecerlos utilizando técnicas de Procesamiento de Lenguaje Natural (NLP) y visualizarlos en Power BI para tomar decisiones de negocio.

## 2. Descripción del Problema
ShopAnalytics enfrenta el desafío de no poder prever retrasos en su cadena de suministro. Las noticias extraídas en la EA2 (desde BBC Mundo) contenían el contexto, pero en formato de texto no estructurado. Un gerente no puede leer miles de noticias diarias para decidir si debe ajustar el inventario de un producto importado. 

## 3. Objetivos
* Transformar el texto extraído aplicando un modelo de limpieza y análisis semántico.
* Asignar un nivel de "Riesgo Logístico" (Alto, Medio, Bajo) a cada noticia basándose en palabras clave.
* Consolidar los datos enriquecidos en una base de datos PostgreSQL.
* Diseñar un tablero en Power BI para que los analistas puedan cruzar los riesgos logísticos con la operación de la empresa.

## 4. Descripción de los Datos
Se cuenta con la tabla `noticias_mercado` en PostgreSQL, alimentada por el scraper de BBC Mundo (EA2). Los datos crudos incluyen `titulo`, `descripcion` y `texto_completo`.

## 5. Solución Propuesta (Transformación y Enriquecimiento)
Se implementó el script `src/modelo.py` el cual:
1. Extrae los registros desde PostgreSQL.
2. Aplica una función de NLP basada en reglas (`aplicar_nlp_basico`), iterando sobre un corpus de palabras clave (ej. "huelga", "paro", "inflación").
3. Asigna un `score_riesgo` cuantitativo y un `nivel_riesgo` categórico.
4. Genera una nueva tabla `noticias_enriquecidas` que mejora drásticamente la utilidad de los datos, pasando de "texto crudo" a "alertas cuantitativas".
5. Crea una Vista SQL (`vw_riesgo_logistico`) optimizada para Power BI.

Además, se implementó el orquestador `src/ejecucion.py`, que lanza el scraper y el modelo secuencialmente, guardando un registro detallado en `auditoria.txt`.

## 6. Metodología CRISP-DM
* **Fase 3 (Preparación de los Datos):** Se extrajo el texto completo y se tokenizó implícitamente al buscar patrones y limpiar mayúsculas/minúsculas.
* **Fase 4 (Modelado):** Aplicación del modelo de inferencia de riesgos (NLP).
* **Fase 5 (Evaluación):** Validación en consola de la distribución de los riesgos encontrados.
* **Fase 6 (Despliegue):** Integración continua en la base de datos y consumo visual mediante Power BI.

## 7. Análisis de Datos Enriquecidos y Power BI
Se conectó exitosamente PostgreSQL con Power BI Desktop utilizando el conector nativo (ODBC/Npgsql).
*El tablero de Power BI demuestra:*
1. **Mapa de Calor de Riesgos:** Qué regiones o temas (ej. "Economía", "Colombia") concentran las noticias de riesgo "Alto".
2. **Volumen de Alertas:** Un indicador clave de cuántas noticias están impactando la cadena de suministro hoy.

*(Nota: En la entrega en plataforma, anexo la imagen del tablero y el archivo .pbix)*

## 8. Conclusiones
* El enriquecimiento de datos transformó un repositorio de noticias estático en un **Sistema de Alerta Temprana**.
* La integración directa desde Python a PostgreSQL y luego a Power BI demuestra que las canalizaciones de datos automatizadas ahorran tiempo y reducen el error humano en la toma de decisiones.

## 9. Bibliografía
* McKinney, W. (2012). *Python for data analysis*. O'Reilly Media, Inc.
* Microsoft. (2023). *Conectar PostgreSQL a Power BI*. Documentación oficial.
* Wirth, R., & Hipp, J. (2000). CRISP-DM: Towards a standard process model for data mining.
