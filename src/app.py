import os
import sqlite3
import pandas as pd
from flask import Flask, jsonify, render_template
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Cargar variables de entorno
load_dotenv()
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/nlp')
def nlp():
    try:
        with engine.connect() as conn:
            # Traer distribución de riesgo logístico (EA3)
            query = "SELECT categoria_riesgo, COUNT(*) as cantidad FROM noticias_enriquecidas GROUP BY categoria_riesgo"
            df = pd.read_sql(query, conn)
            return df.to_json(orient='records')
    except Exception as e:
        print("Error NLP:", e)
        return jsonify([])


@app.route('/api/simulados')
def simulados():
    try:
        # Traer alerta de reabastecimiento priorizado (EA1)
        db_path = os.path.join(os.path.dirname(__file__), '..', 'shopanalytics.db')
        conn = sqlite3.connect(db_path)
        query = "SELECT Categoria, COUNT(*) as cantidad FROM Productos_Enriquecidos WHERE Prioridad_Compra = 'Alta' GROUP BY Categoria"
        df = pd.read_sql(query, conn)
        conn.close()
        return df.to_json(orient='records')
    except Exception as e:
        print("Error Simulados:", e)
        return jsonify([])


@app.route('/api/kaggle')
def kaggle():
    try:
        with engine.connect() as conn:
            # Traer clientes VIP de Olist (Kaggle - EA2)
            query = "SELECT categoria_cliente, COUNT(*) as cantidad FROM vw_olist_clientes_vip GROUP BY categoria_cliente"
            df = pd.read_sql(query, conn)
            return df.to_json(orient='records')
    except Exception as e:
        print("Error Kaggle:", e)
        return jsonify([])


if __name__ == '__main__':
    print("\n========================================================")
    print("🚀 INICIANDO DASHBOARD SHOPANALYTICS S.A.S.")
    print("========================================================\n")
    app.run(debug=True, port=5000)
