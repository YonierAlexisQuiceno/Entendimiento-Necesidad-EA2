import pandas as pd
import sqlite3
import numpy as np
import datetime
# =========================================================
# 1. GENERACIÓN DE DATASET
# =========================================================
print("Generando dataset masivo de (5,000 registros)...")
np.random.seed(42)
num_ventas = 5000

# Datos maestros
ciudades_regiones = {'Bogotá': 'Andina', 'Medellín': 'Andina', 'Cali': 'Pacífica', 'Barranquilla': 'Caribe', 'Bucaramanga': 'Andina'}
categorias_prods = {'Tecnología': ['Laptop ProBook', 'Smartphone X', 'Tablet Y'],
                    'Hogar': ['Cafetera', 'Licuadora', 'Aspiradora'],
                    'Moda': ['Chaqueta', 'Tenis Running', 'Camisa Algodón']}

# Generación aleatoria para simular el historial
fechas = [datetime.date(2023, 1, 1) + datetime.timedelta(days=np.random.randint(0, 365)) for _ in range(num_ventas)]
clientes_ids = [np.random.randint(1, 1000) for _ in range(num_ventas)]
ciudades_seleccionadas = np.random.choice(list(ciudades_regiones.keys()), num_ventas)

# Crear DataFrames Normalizados usando Pandas
# A. Clientes
df_clientes = pd.DataFrame({
    'cliente_id': range(1, 1001),
    'nombre': [f"Cliente_{i}" for i in range(1, 1001)],
    'segmento': np.random.choice(['Estándar', 'Premium', 'Nuevo'], 1000)
})

# B. Regiones
df_regiones = pd.DataFrame({
    'region_id': range(1, len(ciudades_regiones)+1),
    'ciudad': list(ciudades_regiones.keys()),
    'pais': 'Colombia'
})
dict_regiones = {ciudad: i+1 for i, ciudad in enumerate(ciudades_regiones.keys())}

# C. Categorías y Productos
lista_categorias = []
lista_productos = []
cat_id = 1
prod_id = 1
for cat, prods in categorias_prods.items():
    lista_categorias.append({'categoria_id': cat_id, 'nombre_categoria': cat})
    for p in prods:
        lista_productos.append({'producto_id': prod_id, 'nombre': p, 'precio_unitario': np.random.randint(50, 300) * 1000, 'categoria_id': cat_id})
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

    # Crear la venta
    ventas_data.append({'venta_id': venta_id, 'fecha_venta': fechas[venta_id-1], 'cliente_id': cliente, 'region_id': reg_id, 'total_venta': 0})

    # Crear detalles para esa venta (de 1 a 3 productos por ticket)
    num_items = np.random.randint(1, 4)
    total_ticket = 0

    for _ in range(num_items):
        prod = df_productos.sample(1).iloc[0]
        cantidad = np.random.randint(1, 5)
        subtotal = prod['precio_unitario'] * cantidad
        total_ticket += subtotal

        detalles_data.append({
            'detalle_id': detalle_id_counter,
            'venta_id': venta_id,
            'producto_id': prod['producto_id'],
            'cantidad': cantidad,
            'subtotal': subtotal
        })
        detalle_id_counter += 1

    # Actualizar total
    ventas_data[-1]['total_venta'] = total_ticket

df_ventas = pd.DataFrame(ventas_data)
df_detalles = pd.DataFrame(detalles_data)

print(f"✅ Generados {len(df_ventas)} registros de ventas y {len(df_detalles)} ítems vendidos.")
# =========================================================
# 2. CONEXIÓN A SQLITE Y CARGA DE DATOS
# =========================================================
conn = sqlite3.connect('shopanalytics.db')

# Carga masiva usando pandas .to_sql
df_clientes.to_sql('Clientes', conn, if_exists='replace', index=False)
df_regiones.to_sql('Regiones', conn, if_exists='replace', index=False)
df_categorias.to_sql('Categorias', conn, if_exists='replace', index=False)
df_productos.to_sql('Productos', conn, if_exists='replace', index=False)
df_ventas.to_sql('Ventas', conn, if_exists='replace', index=False)
df_detalles.to_sql('Detalle_Ventas', conn, if_exists='replace', index=False)

print("✅ Base de datos 'shopanalytics.db' creada y poblada exitosamente.\n")
# =========================================================
# 3. VERIFICACIÓN: CONSULTA ANALÍTICA DEL NEGOCIO
# =========================================================
print("📊 RESULTADO DEL ANÁLISIS: Ingresos Totales por Categoría\n")

query = '''
    SELECT
        c.nombre_categoria AS Categoria,
        COUNT(DISTINCT v.venta_id) AS Total_Tickets,
        SUM(d.cantidad) AS Unidades_Vendidas,
        SUM(d.subtotal) AS Ingresos_Totales
    FROM Detalle_Ventas d
    JOIN Ventas v ON d.venta_id = v.venta_id
    JOIN Productos p ON d.producto_id = p.producto_id
    JOIN Categorias c ON p.categoria_id = c.categoria_id
    GROUP BY c.nombre_categoria
    ORDER BY Ingresos_Totales DESC;
'''

# Ejecutar y mostrar con Pandas
df_resultados = pd.read_sql_query(query, conn)

# Formatear a moneda colombiana para mejor presentación
df_resultados['Ingresos_Totales'] = df_resultados['Ingresos_Totales'].apply(lambda x: f"${x:,.0f}")
display(df_resultados)

conn.close()