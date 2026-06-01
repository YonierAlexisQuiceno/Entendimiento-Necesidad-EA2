"""
Script para ingestar datos de Olist (Kaggle) a PostgreSQL.
"""
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Conexión a PostgreSQL
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

if not all([db_user, db_pass, db_host, db_port, db_name]):
    raise ValueError("Faltan credenciales de PostgreSQL en el archivo .env. Asegúrate de configurarlo.")

db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)

def ingestar_csv(archivo, nombre_tabla, chunksize=1000, limite=5000):
    ruta = os.path.join("data", archivo) # Se asume que los CSV están en 'data' (antes 'archive')
    # O en 'archive' si no se renombró
    ruta_archive = os.path.join("archive", archivo)
    ruta_final = ruta if os.path.exists(ruta) else ruta_archive

    if not os.path.exists(ruta_final):
        print(f"[!] Archivo {ruta_final} no encontrado. Saltando...")
        return
    
    print(f"[*] Ingestando {ruta_final} en tabla '{nombre_tabla}' (Límite: {limite})...")
    
    # Leer un chunk pequeño para ahorrar memoria
    df = pd.read_csv(ruta_final, nrows=limite)
    df.to_sql(nombre_tabla, engine, if_exists='replace', index=False)
    print(f"[+] Éxito: {len(df)} registros insertados en {nombre_tabla}.")

if __name__ == "__main__":
    print("Iniciando Ingesta de Kaggle (Olist)...")
    ingestar_csv("olist_customers_dataset.csv", "clientes")
    ingestar_csv("olist_products_dataset.csv", "productos")
    ingestar_csv("olist_orders_dataset.csv", "ordenes")
    ingestar_csv("olist_order_items_dataset.csv", "items_orden")
    
    print("\n[ENRIQUECIMIENTO] Creando vista analítica vw_olist_clientes_vip...")
    from sqlalchemy import text
    vista_sql = """
    CREATE OR REPLACE VIEW vw_olist_clientes_vip AS
    SELECT 
        c.customer_id,
        c.customer_city,
        c.customer_state,
        COUNT(o.order_id) as total_ordenes,
        CASE 
            WHEN COUNT(o.order_id) > 1 THEN 'VIP'
            ELSE 'Estandar'
        END as categoria_cliente
    FROM clientes c
    LEFT JOIN ordenes o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_city, c.customer_state;
    """
    try:
        with engine.connect() as conn:
            conn.execute(text(vista_sql))
            conn.commit()
        print("[+] Vista vw_olist_clientes_vip generada en PostgreSQL.")
    except Exception as e:
        print(f"[ERROR] No se pudo crear la vista: {e}")
        
    print("Ingesta completada.")
