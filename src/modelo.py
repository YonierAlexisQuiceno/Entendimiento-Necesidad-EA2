import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import re

def aplicar_nlp_basico(texto):
    """
    Función de análisis de texto simple (NLP basado en reglas) 
    para extraer sentimiento logístico y categorizar riesgo.
    """
    if not texto or pd.isna(texto):
        return "Bajo", 0
    
    texto = str(texto).lower()
    
    # Palabras clave de alto riesgo logístico
    keywords_alto = ["huelga", "escasez", "retraso", "crisis", "guerra", "bloqueo", "paro", "cierre", "conflicto"]
    # Palabras clave de riesgo medio
    keywords_medio = ["inflación", "costos", "protesta", "aduanas", "restricción", "clima", "tormenta"]
    
    score = 0
    for kw in keywords_alto:
        score += len(re.findall(r'\b' + kw + r'\b', texto)) * 3
    for kw in keywords_medio:
        score += len(re.findall(r'\b' + kw + r'\b', texto)) * 1

    if score >= 5:
        return "Alto", score
    elif score >= 2:
        return "Medio", score
    else:
        return "Bajo", score

def ejecutar_transformacion():
    print("="*60)
    print(" INICIANDO TRANSFORMACIÓN Y ENRIQUECIMIENTO (EA3) - NLP")
    print("="*60)
    
    load_dotenv()
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    if not all([db_user, db_pass, db_host, db_port, db_name]):
        raise ValueError("Faltan credenciales de PostgreSQL en el archivo .env.")

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)

    try:
        with engine.connect() as conn:
            print("[*] Conectando a PostgreSQL y leyendo noticias crudas...")
            # Leer noticias crudas
            df_noticias = pd.read_sql("SELECT * FROM noticias_mercado", conn)
            
            if df_noticias.empty:
                print("[-] No hay noticias para procesar.")
                return

            print("[*] Aplicando modelo de transformación NLP para detectar riesgo logístico...")
            
            # Aplicar transformación
            resultados = df_noticias['texto_completo'].apply(aplicar_nlp_basico)
            df_noticias['nivel_riesgo'] = [r[0] for r in resultados]
            df_noticias['score_riesgo'] = [r[1] for r in resultados]
            
            # Dejar solo las columnas enriquecidas para la nueva tabla
            df_enriquecido = df_noticias[['id', 'titulo', 'fecha_publicacion', 'temas_relacionados', 'nivel_riesgo', 'score_riesgo', 'url']]
            
            print("[*] Guardando tabla de noticias_enriquecidas en PostgreSQL...")
            df_enriquecido.to_sql("noticias_enriquecidas", engine, if_exists='replace', index=False)
            
            print(f"[+] Éxito: {len(df_enriquecido)} noticias enriquecidas guardadas.")
            
            # Crear Vista Analítica para Power BI
            print("[*] Creando Vista Analítica (vw_riesgo_logistico) para Power BI...")
            vista_sql = """
            CREATE OR REPLACE VIEW vw_riesgo_logistico AS
            SELECT 
                n.id AS noticia_id,
                n.titulo,
                n.nivel_riesgo,
                n.score_riesgo,
                n.temas_relacionados,
                CURRENT_DATE AS fecha_analisis
            FROM noticias_enriquecidas n
            WHERE n.score_riesgo > 0
            ORDER BY n.score_riesgo DESC;
            """
            conn.execute(vista_sql)
            print("[+] Vista SQL creada exitosamente.")
            
    except Exception as e:
        print(f"[ERROR CRÍTICO] Fallo en la transformación: {e}")

if __name__ == "__main__":
    ejecutar_transformacion()
