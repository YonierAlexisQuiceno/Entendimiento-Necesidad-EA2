import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

# Cargar credenciales desde .env
load_dotenv()

user = os.getenv("DB_USER")
pwd = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

if not all([user, pwd, host, port, db_name]):
    raise ValueError("Faltan credenciales de PostgreSQL en el archivo .env. Asegúrate de configurarlo.")

try:
    # Conectarse a la base de datos por defecto 'postgres' para poder crear la nueva BD
    conn = psycopg2.connect(user=user, password=pwd, host=host, port=port, database="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
    exists = cur.fetchone()
    
    if not exists:
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"Base de datos '{db_name}' creada exitosamente.")
    else:
        print(f"La base de datos '{db_name}' ya existe.")
        
    cur.close()
    conn.close()
    print("[OK] Conexión a PostgreSQL validada correctamente.")
except Exception as e:
    print(f"Error al conectar con PostgreSQL o crear la base de datos: {e}")
