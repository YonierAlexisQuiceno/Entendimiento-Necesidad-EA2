# S30 - Entrega 1: Entendimiento de la Necesidad EA1

**Estudiante:** Yonier Alexis Quiceno Rodríguez  
**Universidad:** IU Digital de Antioquia  
**Programa:** Ingeniería de Software y Datos  
**Grupo:** PREICA2601B020089 - Programación para Análisis de Datos  

**Docente:** Ana Maria Lopez  
**Fecha:** 02 de abril de 2026

---

# Definición de la Necesidad

## Caso de Estudio Seleccionado

El caso de estudio seleccionado corresponde a una empresa de comercio electrónico, dedicada a la venta de productos de tecnología, hogar y moda a través de una plataforma digital.

La empresa opera en Colombia y atiende a miles de clientes activos, generando diariamente un volumen masivo de transacciones de venta.

La organización enfrenta problemas recurrentes de:

- Desabastecimiento en productos de alta demanda.
- Overstock en artículos de baja rotación.

Esto genera:

- Pérdidas económicas significativas.
- Clientes insatisfechos.
- Costos elevados de almacenamiento.

La gerencia ha identificado la necesidad de implementar un sistema de análisis de datos estructurado y escalable (basado en datasets masivos estilo Kaggle / Datos Abiertos) que permita tomar decisiones informadas sobre la gestión del inventario.

---

# Necesidad del Negocio

La necesidad principal del negocio consiste en optimizar la gestión del inventario mediante el análisis descriptivo y predictivo de los datos de ventas históricos, el comportamiento del cliente y la distribución geográfica de las compras.

## Objetivo General

Desarrollar un modelo de análisis de datos basado en la metodología **CRISP-DM** que permita:

- Optimizar inventario.
- Reducir pérdidas por desabastecimiento y sobrestock.
- Mejorar la satisfacción del cliente.

## Objetivos Específicos

- Analizar los patrones de ventas históricas por categoría y región para identificar tendencias de demanda.
- Identificar los productos con mayor rotación (Top Ventas) y los que presentan mayor riesgo de estancamiento.
- Diseñar un modelo de datos escalable que permita la ingesta, limpieza y consulta eficiente de miles de registros simulando entornos de Big Data.

---

# Requerimientos del Negocio

| N° | Requerimiento | Descripción | Prioridad |
|---|---|---|---|
| R1 | Integración masiva de datos | Consolidar datos históricos masivos (estilo dataset Kaggle) en una base de datos relacional. | Alta |
| R2 | Modelo Relacional | Diseñar un esquema de datos normalizado (Clientes, Productos, Ventas, Regiones) para evitar redundancias. | Alta |
| R3 | Análisis descriptivo | Generar consultas SQL que extraigan las ventas por categoría y región. | Alta |
| R4 | Automatización (ETL) | Crear un script en Python (Pandas) para la generación, transformación y carga de la base de datos. | Media |

---

# Diseño de la Necesidad

## Traducción de Requisitos al Plan Analítico

A partir de los requerimientos identificados, se diseña un plan estructurado que traduce cada necesidad del negocio en tareas de procesamiento de datos.

Se simulará la descarga de un dataset masivo, el cual será procesado mediante librerías de Python y cargado en una base de datos analítica.

## Diagrama de Flujo del Proceso CRISP-DM

El siguiente diagrama representa el flujo de trabajo de las fases 1 y 2 de CRISP-DM aplicadas al caso de estudio.

> Nota: A continuación se describe el diagrama de flujo del proceso.

---

# Identificación de Fuentes de Datos

| Fuente | Tipo | Datos Contenidos | Formato / Tecnología |
|---|---|---|---|
| Dataset Histórico (Kaggle/Simulado) | Externa/Masiva | Ventas históricas, demografía, productos, transacciones. | CSV / DataFrame Pandas |
| Base de Datos Analítica | Interna | Estructura normalizada con llaves primarias y foráneas. | Relacional (SQLite) |

---

# Modelo de Datos

## Esquema de la Base de Datos

Se diseña un esquema de base de datos relacional en PostgreSQL que centraliza la información de ventas, inventario y clientes.

El modelo contempla las siguientes entidades principales y sus relaciones.

## Entidades y Atributos

### Regiones

- `region_id` (PK)
- `ciudad`
- `pais`

### Clientes

- `cliente_id` (PK)
- `nombre`
- `segmento`

### Categorias

- `categoria_id` (PK)
- `nombre_categoria`

### Productos

- `producto_id` (PK)
- `nombre`
- `precio_unitario`
- `categoria_id` (FK)

### Ventas (Encabezado)

- `venta_id` (PK)
- `fecha_venta`
- `cliente_id` (FK)
- `region_id` (FK)

### Detalle_Ventas

- `detalle_id` (PK)
- `venta_id` (FK)
- `producto_id` (FK)
- `cantidad`
- `subtotal`

---

# Relaciones entre Entidades

- **Regiones ←→ Ventas (1:N):** Una región puede registrar múltiples ventas.
- **Clientes ←→ Ventas (1:N):** Un cliente puede realizar múltiples compras a lo largo del tiempo.
- **Categorias ←→ Productos (1:N):** Una categoría agrupa múltiples productos del catálogo.
- **Ventas ←→ Detalle_Ventas (1:N):** Un ticket de venta puede contener múltiples ítems.
- **Productos ←→ Detalle_Ventas (1:N):** Un producto puede aparecer en múltiples transacciones.

---

# Conexión y Carga de Prueba de la Base de Datos

## Tecnología Seleccionada

Para abordar la recomendación de trabajar con volúmenes de datos más extensos (simulando datasets gubernamentales o de Kaggle), se implementó la solución utilizando **Google Colab**.

### Tecnologías Utilizadas

- **Lenguaje:** Python 3.
- **Procesamiento:** Librerías Pandas y NumPy para la generación y normalización de un dataset masivo de más de 5,000 registros.
- **Motor de Base de Datos:** SQLite3.

SQLite3 permite crear una base de datos relacional embebida dentro del mismo entorno de Colab, ideal para prototipado rápido y analítica sin requerir configuraciones complejas de servidores externos.

---

# Carga de Datos de Prueba

A continuación, se presenta la descripción del código implementado en el archivo `.ipynb` adjunto a esta entrega.

El script realiza las siguientes acciones:

1. Genera sintéticamente un dataset transaccional extenso (+5,000 registros) simulando ventas de e-commerce.
2. Divide (normaliza) el DataFrame plano en las diferentes tablas descritas en el modelo de datos:
   - Clientes
   - Regiones
   - Categorías
   - Productos
   - Ventas
   - Detalles
3. Establece conexión a `shopanalytics.db` vía SQLite.
4. Carga los DataFrames en sus respectivas tablas SQL utilizando `to_sql()`.

---

# Verificación y Consulta Analítica

Para comprobar la funcionalidad del modelo y responder a la necesidad del negocio, se ejecutó una consulta SQL cruzando cuatro tablas:

- `Detalle_Ventas`
- `Productos`
- `Categorias`
- `Ventas`

El objetivo fue identificar el rendimiento y los ingresos totales por categoría, demostrando la eficacia del modelo relacional.

> El código fuente ejecutable se encuentra en el archivo Jupyter Notebook / Colab adjunto.

---

# Conclusiones

A lo largo de este primer entregable se aplicaron las fases 1 y 2 de la metodología **CRISP-DM** al caso de estudio de la empresa.

Las principales conclusiones son:

- Se identificó con claridad la necesidad del negocio y se amplió el alcance para soportar análisis masivos de datos (estilo Kaggle).
- El diseño del proceso integró el ecosistema de Python (Pandas + SQLite), proporcionando una hoja de ruta técnica sólida.
- El modelo de datos relacional refleja eficientemente las entidades del negocio, eliminando redundancias y preparando el terreno para el cruce de variables.
- La carga de prueba demostró que el modelo es capaz de ingerir y consultar miles de registros en segundos.

Como próximo paso, se procederá a la fase 3 de CRISP-DM (**Preparación de los Datos**) enfocada en limpieza de valores nulos y atípicos en escenarios reales.

---

# Recursos

## Video

```text
https://youtu.be/rUzqwfYEEmU
```

## Google Colab

```text
https://colab.research.google.com/drive/1H-lqJQvo8EWCbFm0I-DVA_AKeQa9AxZi?usp=sharing
```

---

# Referencias

- Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS Inc, 9(13), 1-73.

  > Documento fundamental que detalla las fases de la metodología CRISP-DM.

- Provost, F., & Fawcett, T. (2013). *Data Science for Business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.

  > Base teórica para la formulación de problemas de negocio y minería de datos en entornos empresariales.

