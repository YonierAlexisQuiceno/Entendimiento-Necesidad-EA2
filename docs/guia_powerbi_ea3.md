# Guía de Conexión: PostgreSQL a Power BI

Dado que un archivo `.pbix` es un formato binario propietario que debe generarse dentro del software visual Power BI Desktop, aquí tienes las instrucciones de 2 minutos para armar el tablero perfecto que te dará la nota máxima en la EA3.

## Paso 1: Conectar Power BI a tu Base de Datos
1. Abre Power BI Desktop.
2. Ve a **Inicio > Obtener datos > PostgreSQL database**.
3. En la ventana que aparece, ingresa:
   * **Servidor:** `localhost`
   * **Base de datos:** `shopanalytics`
4. En **Modo de Conectividad**, selecciona **DirectQuery** (para que tu tablero se actualice en tiempo real cada vez que corras tu scraper de Python). Haz clic en Aceptar.
5. Cuando te pida credenciales, ingresa tu usuario (ej. `postgres`) y contraseña (ej. `12345`).

## Paso 2: Seleccionar los Datos Enriquecidos
* En el Navegador, marca la vista **`vw_riesgo_logistico`** que el script `modelo.py` creó automáticamente.
* Dale clic a **Cargar**.

## Paso 3: Crear los Gráficos Visuales (El Tablero)

### Gráfico 1: "Concentración de Riesgo por Tema"
1. Arrastra un gráfico circular (Pie chart) al lienzo.
2. En **Leyenda**, arrastra la columna `temas_relacionados`.
3. En **Valores**, arrastra `noticia_id` (y en el menú de la variable pon "Recuento").
*Este gráfico mostrará qué temas abarcan el mayor riesgo.*

### Gráfico 2: "Gravedad del Riesgo Logístico"
1. Arrastra un gráfico de columnas apiladas.
2. En el Eje X pon `nivel_riesgo` (Alto, Medio, Bajo).
3. En el Eje Y pon "Recuento de `noticia_id`".
*Esto permite a gerencia ver cuántas alarmas rojas (Riesgo Alto) existen hoy.*

### Indicador Clave (KPI)
1. Arrastra una "Tarjeta" (Card visual).
2. Arrastra la columna `score_riesgo` a la tarjeta, y configúrala como "Promedio" o "Suma". 
*Esto te dará el score total de peligrosidad del mercado de hoy.*

## Paso 4: Exportar
1. Toma una captura de pantalla bonita del tablero para pegarla en tu documento PDF (donde dice la nota).
2. Ve a **Archivo > Guardar como** y guárdalo como `Quiceno_Rodriguez_Yonier_Alexis_EA3.pbix`.
3. ¡Sube tu entrega a la plataforma!
