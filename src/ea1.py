# -*- coding: utf-8 -*-
"""
Modulo 1: Entendimiento de la Necesidad EA1 (Mejorado)
Estudiante: Yonier Alexis Quiceno Rodriguez
Universidad: IU Digital de Antioquia
Programa: Ingenieria de Software y Datos
Grupo: PREICA2601B020089 - Programacion para Analisis de Datos
Docente: Ana Maria Lopez

Descripcion: Script de simulacion de e-commerce e ingesta local en SQLite.
Incluye columnas de inventario activo, validaciones de integridad de datos y
consultas analiticas avanzadas para toma de decisiones.
"""

import pandas as pd
import sqlite3
import numpy as np
import datetime
import sys

# Forzar codificacion UTF-8 para evitar errores de consola en Windows
try:
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

print("======================================================================")
print("[INFO] INICIANDO PIPELINE ANALITICO DE SHOPANALYTICS S.A.S.")
print("======================================================================")

# =========================================================
# 1. GENERACION DE DATASET SIMULADO (TRANSPARENTE Y CONTROLADO)
# =========================================================
print("\n[1/4] Generando dataset transaccional simulado (+5,000 registros)...")
np.random.seed(42)
num_ventas = 5000

# Datos maestros
ciudades_regiones = {
    'Bogota': 'Andina', 
    'Medellin': 'Andina', 
    'Cali': 'Pacifica', 
    'Barranquilla': 'Caribe', 
    'Bucaramanga': 'Andina'
}
categorias_prods = {
    'Tecnologia': ['Laptop ProBook', 'Smartphone X', 'Tablet Y'],
    'Hogar': ['Cafetera', 'Licuadora', 'Aspiradora'],
    'Moda': ['Chaqueta', 'Tenis Running', 'Camisa Algodon']
}

# Generacion aleatoria para simular el historial
fechas = [datetime.date(2025, 1, 1) + datetime.timedelta(days=int(np.random.randint(0, 365))) for _ in range(num_ventas)]
clientes_ids = [int(np.random.randint(1, 1001)) for _ in range(num_ventas)]
ciudades_seleccionadas = np.random.choice(list(ciudades_regiones.keys()), num_ventas)

# Crear DataFrames Normalizados usando Pandas
# A. Clientes
df_clientes = pd.DataFrame({
    'cliente_id': range(1, 1001),
    'nombre': [f"Cliente_{i}" for i in range(1, 1001)],
    'segmento': np.random.choice(['Estandar', 'Premium', 'Nuevo'], 1000)
})

# B. Regiones
df_regiones = pd.DataFrame({
    'region_id': range(1, len(ciudades_regiones)+1),
    'ciudad': list(ciudades_regiones.keys()),
    'pais': 'Colombia'
})
dict_regiones = {ciudad: i+1 for i, ciudad in enumerate(ciudades_regiones.keys())}

# C. Categorias y Productos (Enriquecidos con variables de control de inventario)
lista_categorias = []
lista_productos = []
cat_id = 1
prod_id = 1

for cat, prods in categorias_prods.items():
    lista_categorias.append({'categoria_id': cat_id, 'nombre_categoria': cat})
    for p in prods:
        # Definir stock simulado y puntos de reorden estrategicos
        stock_simulado = int(np.random.randint(5, 120))  # Rango de stock en almacen
        punto_reorden_simulado = int(np.random.randint(15, 30))  # Nivel minimo de seguridad
        
        lista_productos.append({
            'producto_id': prod_id, 
            'nombre': p, 
            'precio_unitario': int(np.random.randint(50, 300) * 1000), 
            'categoria_id': cat_id,
            'stock_actual': stock_simulado,
            'punto_reorden': punto_reorden_simulado
        })
        prod_id += 1
    cat_id += 1

df_categorias = pd.DataFrame(lista_categorias)
df_productos = pd.DataFrame(lista_productos)

# D. Ventas y Detalles (Transaccional)
ventas_data = []
detalles_data = []
detalle_id_counter = 1

for venta_id in range(1, num_ventas + 1):
    cliente = np.random.choice(clientes_ids)
    ciudad = ciudades_seleccionadas[venta_id - 1]
    reg_id = dict_regiones[ciudad]

    # Crear la venta (encabezado)
    ventas_data.append({
        'venta_id': venta_id, 
        'fecha_venta': fechas[venta_id-1], 
        'cliente_id': int(cliente), 
        'region_id': reg_id, 
        'total_venta': 0.0
    })

    # Crear detalles para esa venta (de 1 a 3 productos por ticket)
    num_items = np.random.randint(1, 4)
    total_ticket = 0

    for _ in range(num_items):
        prod = df_productos.sample(1).iloc[0]
        cantidad = int(np.random.randint(1, 5))
        subtotal = int(prod['precio_unitario'] * cantidad)
        total_ticket += subtotal

        detalles_data.append({
            'detalle_id': detalle_id_counter,
            'venta_id': venta_id,
            'producto_id': int(prod['producto_id']),
            'cantidad': cantidad,
            'subtotal': subtotal
        })
        detalle_id_counter += 1

    # Actualizar total de la venta en el encabezado
    ventas_data[-1]['total_venta'] = float(total_ticket)

df_ventas = pd.DataFrame(ventas_data)
df_detalles = pd.DataFrame(detalles_data)

# Agregar un producto estancado (Legacy) que no tiene ventas simuladas para comprobar el Analisis B
df_stagnant = pd.DataFrame([{
    'producto_id': 10,
    'nombre': 'Teclado Mecanico Retro',
    'precio_unitario': 180000,
    'categoria_id': 1,
    'stock_actual': 95,
    'punto_reorden': 15
}])
df_productos = pd.concat([df_productos, df_stagnant], ignore_index=True)

print(f"[OK] Se generaron artificialmente {len(df_ventas)} ventas y {len(df_detalles)} items transaccionales.")

# =========================================================
# 2. CONEXION A SQLITE Y CARGA DE DATOS
# =========================================================
print("\n[2/4] Conectando a SQLite e ingestando tablas normalizadas...")
conn = sqlite3.connect('shopanalytics.db')

# Carga masiva usando pandas .to_sql
df_clientes.to_sql('Clientes', conn, if_exists='replace', index=False)
df_regiones.to_sql('Regiones', conn, if_exists='replace', index=False)
df_categorias.to_sql('Categorias', conn, if_exists='replace', index=False)
df_productos.to_sql('Productos', conn, if_exists='replace', index=False)
df_ventas.to_sql('Ventas', conn, if_exists='replace', index=False)
df_detalles.to_sql('Detalle_Ventas', conn, if_exists='replace', index=False)

print("[OK] Base de datos local 'shopanalytics.db' creada e ingestada con exito.")

# =========================================================
# 3. VALIDACIONES AUTOMATICAS DE CALIDAD DE DATOS E INTEGRIDAD
# =========================================================
print("\n[3/4] Ejecutando pruebas de control de calidad e integridad de datos...")

errores_encontrados = 0

# Prueba A: Conteo e Igualdad de Registros
tablas_conteos = {
    'Clientes': len(df_clientes),
    'Regiones': len(df_regiones),
    'Categorias': len(df_categorias),
    'Productos': len(df_productos),
    'Ventas': len(df_ventas),
    'Detalle_Ventas': len(df_detalles)
}

print("  -> Verificando conteo de filas:")
for tabla, expected_count in tablas_conteos.items():
    db_count = pd.read_sql_query(f"SELECT COUNT(*) as cant FROM {tabla}", conn).iloc[0]['cant']
    if db_count == expected_count:
        print(f"     [PASS] Tabla '{tabla}': {db_count} registros persistidos.")
    else:
        print(f"     [FAIL] Tabla '{tabla}': Esperados {expected_count}, pero en BD hay {db_count}.")
        errores_encontrados += 1

# Prueba B: Unicidad de Llaves Primarias
print("  -> Comprobando unicidad de llaves primarias:")
pks = {
    'Clientes': 'cliente_id',
    'Regiones': 'region_id',
    'Categorias': 'categoria_id',
    'Productos': 'producto_id',
    'Ventas': 'venta_id',
    'Detalle_Ventas': 'detalle_id'
}

for tabla, pk in pks.items():
    dups = pd.read_sql_query(f"SELECT COUNT({pk}) - COUNT(DISTINCT {pk}) as dups FROM {tabla}", conn).iloc[0]['dups']
    if dups == 0:
        print(f"     [PASS] Tabla '{tabla}' llave primaria '{pk}' es unica.")
    else:
        print(f"     [FAIL] Tabla '{tabla}' tiene {dups} registros duplicados en PK '{pk}'.")
        errores_encontrados += 1

# Prueba C: Consistencia Referencial (Llaves Foraneas)
print("  -> Evaluando integridad referencial (llaves foraneas):")

# Ventas -> Clientes
huérfanos_clientes = pd.read_sql_query('''
    SELECT COUNT(v.venta_id) as cant 
    FROM Ventas v 
    LEFT JOIN Clientes c ON v.cliente_id = c.cliente_id 
    WHERE c.cliente_id IS NULL
''', conn).iloc[0]['cant']

if huérfanos_clientes == 0:
    print("     [PASS] Ventas -> Clientes: Cero huérfanos.")
else:
    print(f"     [FAIL] Ventas -> Clientes: Se encontraron {huérfanos_clientes} ventas huerfanas.")
    errores_encontrados += 1

# Ventas -> Regiones
huérfanos_regiones = pd.read_sql_query('''
    SELECT COUNT(v.venta_id) as cant 
    FROM Ventas v 
    LEFT JOIN Regiones r ON v.region_id = r.region_id 
    WHERE r.region_id IS NULL
''', conn).iloc[0]['cant']

if huérfanos_regiones == 0:
    print("     [PASS] Ventas -> Regiones: Cero huérfanos.")
else:
    print(f"     [FAIL] Ventas -> Regiones: Se encontraron {huérfanos_regiones} ventas huerfanas.")
    errores_encontrados += 1

# Detalle_Ventas -> Ventas
huérfanos_ventas = pd.read_sql_query('''
    SELECT COUNT(d.detalle_id) as cant 
    FROM Detalle_Ventas d 
    LEFT JOIN Ventas v ON d.venta_id = v.venta_id 
    WHERE v.venta_id IS NULL
''', conn).iloc[0]['cant']

if huérfanos_ventas == 0:
    print("     [PASS] Detalle_Ventas -> Ventas: Cero huérfanos.")
else:
    print(f"     [FAIL] Detalle_Ventas -> Ventas: Se encontraron {huérfanos_ventas} detalles huérfanos.")
    errores_encontrados += 1

# Detalle_Ventas -> Productos
huérfanos_productos = pd.read_sql_query('''
    SELECT COUNT(d.detalle_id) as cant 
    FROM Detalle_Ventas d 
    LEFT JOIN Productos p ON d.producto_id = p.producto_id 
    WHERE p.producto_id IS NULL
''', conn).iloc[0]['cant']

if huérfanos_productos == 0:
    print("     [PASS] Detalle_Ventas -> Productos: Cero huérfanos.")
else:
    print(f"     [FAIL] Detalle_Ventas -> Productos: Se encontraron {huérfanos_productos} detalles huérfanos.")
    errores_encontrados += 1

if errores_encontrados == 0:
    print("[INFO-CALIDAD] Pruebas finalizadas. Integridad y calidad del modelo: 100% CORRECTA.")
else:
    print(f"[ALERTA-CALIDAD] Se encontraron {errores_encontrados} errores en las pruebas de calidad.")

# =========================================================
# 4. CONSULTAS ANALITICAS ORIENTADAS A LA TOMA DE DECISIONES
# =========================================================
print("\n[4/4] Ejecutando consultas analiticas orientadas a la toma de decisiones...")

# --- CONSULTA A: Alerta Preventiva de Reabastecimiento (Evita Stockouts) ---
print("\n" + "="*80)
print("[ANÁLISIS A] ALERTA PREVENTIVA DE REABASTECIMIENTO (KPI: Quiebre de Stock < 20%)")
print("Decisión: Comprar prioridad alta para evitar perdida de ventas.")
print("="*80)

query_reabastecimiento = '''
    SELECT 
        p.producto_id, 
        p.nombre AS Producto, 
        c.nombre_categoria AS Categoria,
        p.stock_actual AS Stock_Disponible, 
        p.punto_reorden AS Nivel_Seguridad,
        (p.punto_reorden - p.stock_actual) AS Deficit_a_Pedir
    FROM Productos p
    JOIN Categorias c ON p.categoria_id = c.categoria_id
    WHERE p.stock_actual <= p.punto_reorden
    ORDER BY Deficit_a_Pedir DESC;
'''
df_reabast = pd.read_sql_query(query_reabastecimiento, conn)
if not df_reabast.empty:
    print(df_reabast.to_string(index=False))
else:
    print("  -> Todos los productos se encuentran por encima de los niveles de seguridad de inventario.")

# --- CONSULTA B: Alerta de Riesgo de Estancamiento y Sobrestock ---
print("\n" + "="*80)
print("[ANÁLISIS B] ALERTA DE RIESGO DE ESTANCAMIENTO Y OVERSTOCK (KPI: Reduccion Exceso Stock 15%)")
print("Decisión: Lanzar ofertas comerciales para liberar capital inmovilizado.")
print("="*80)

query_overstock = '''
    SELECT 
        p.nombre AS Producto, 
        p.stock_actual AS Stock_Almacenado,
        COALESCE(SUM(d.cantidad), 0) AS Unidades_Vendidas,
        (p.stock_actual - COALESCE(SUM(d.cantidad), 0)) AS Inventario_Excedente
    FROM Productos p
    LEFT JOIN Detalle_Ventas d ON p.producto_id = d.producto_id
    GROUP BY p.producto_id
    HAVING Unidades_Vendidas < 50 AND Stock_Almacenado > 50
    ORDER BY Stock_Almacenado DESC;
'''
df_over = pd.read_sql_query(query_overstock, conn)
if not df_over.empty:
    print(df_over.to_string(index=False))
else:
    print("  -> No se detectaron productos con alto sobrestock y baja rotacion critica.")

# --- CONSULTA C: Rotación e Ingresos por Categoría de Productos ---
print("\n" + "="*80)
print("[ANÁLISIS C] ROTACION E INGRESOS TOTALES POR CATEGORIA DE PRODUCTO")
print("Decisión: Optimizar distribucion fisica de almacenamiento principal (bodegas centrales).")
print("="*80)

query_rotacion = '''
    SELECT 
        c.nombre_categoria AS Categoria,
        COUNT(DISTINCT v.venta_id) AS Transacciones,
        SUM(d.cantidad) AS Unidades_Vendidas,
        SUM(d.subtotal) AS Ingresos_Totales
    FROM Detalle_Ventas d
    JOIN Ventas v ON d.venta_id = v.venta_id
    JOIN Productos p ON d.producto_id = p.producto_id
    JOIN Categorias c ON p.categoria_id = c.categoria_id
    GROUP BY c.nombre_categoria
    ORDER BY Unidades_Vendidas DESC;
'''
df_rot = pd.read_sql_query(query_rotacion, conn)
# Formatear montos para presentacion estetica
df_rot['Ingresos_Totales'] = df_rot['Ingresos_Totales'].apply(lambda x: f"${x:,.0f} COP")
print(df_rot.to_string(index=False))

# --- CONSULTA D: Concentración Geográfica de Ventas para Distribución Regional ---
print("\n" + "="*80)
print("[ANÁLISIS D] CONCENTRACION GEOGRAFICA DE VENTAS (KPI: Disponibilidad Regional > 95%)")
print("Decisión: Abrir o pre-distribuir inventario en bodegas locales de alto volumen.")
print("="*80)

query_geografia = '''
    SELECT 
        r.ciudad AS Ciudad, 
        r.pais AS Pais,
        COUNT(DISTINCT v.venta_id) AS Cantidad_Pedidos,
        SUM(v.total_venta) AS Facturacion_Total
    FROM Ventas v
    JOIN Regiones r ON v.region_id = r.region_id
    GROUP BY r.ciudad
    ORDER BY Facturacion_Total DESC;
'''
df_geo = pd.read_sql_query(query_geografia, conn)
# Formatear montos para presentacion estetica
df_geo['Facturacion_Total'] = df_geo['Facturacion_Total'].apply(lambda x: f"${x:,.0f} COP")
print(df_geo.to_string(index=False))

conn.close()
print("\n======================================================================")
print("[INFO] PIPELINE ANALITICO FINALIZADO CON EXITO.")
print("======================================================================")