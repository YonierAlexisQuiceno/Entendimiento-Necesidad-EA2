import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

passwords_to_try = ["", "postgres", "admin", "1234", "password", "root", "shopanalytics"]
user = "postgres"
host = "localhost"
port = "5432"
db_name = "shopanalytics"

success_pwd = None
for pwd in passwords_to_try:
    try:
        conn = psycopg2.connect(user=user, password=pwd, host=host, port=port)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
        exists = cur.fetchone()
        if not exists:
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f"Base de datos {db_name} creada exitosamente.")
        else:
            print(f"La base de datos {db_name} ya existe.")
            
        cur.close()
        conn.close()
        success_pwd = pwd
        print(f"SUCCESS_PASSWORD_FOUND:{pwd}")
        break
    except Exception as e:
        pass

if success_pwd is None:
    print("NO_PASSWORD_WORKED")
