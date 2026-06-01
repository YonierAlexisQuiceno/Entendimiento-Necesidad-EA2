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
    print("Ingesta completada.")
