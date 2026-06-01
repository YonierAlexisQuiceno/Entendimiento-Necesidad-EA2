"""
Módulo de Transformación y Enriquecimiento de Datos (EA3)
Autor: Yonier Alexis Quiceno Rodríguez
Descripción: Aplica un modelo NLP basado en reglas para clasificar noticias
escrapeadas según su nivel y categoría de riesgo logístico.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import re


def aplicar_nlp_basico(texto):
    """
    Función de análisis de texto simple (NLP basado en reglas) 
    para extraer sentimiento logístico y categorizar riesgo.
    
    Returns:
        tuple: (nivel_riesgo, score_riesgo, categoria_dominante)
    """
    if not texto or pd.isna(texto):
        return "Bajo", 0, "Ninguna"
    
    texto = str(texto).lower()
    
    # Diccionarios de palabras clave por categoría de riesgo
    riesgos = {
        "Geopolítico": ["guerra", "conflicto", "bloqueo", "sanciones", "frontera",
                         "geopolítica", "tensión", "gobierno", "militar", "diplomacia"],
        "Operativo":   ["huelga", "escasez", "retraso", "paro", "cierre", "clima",
                         "tormenta", "desastre", "logística", "puerto", "transporte"],
        "Financiero":  ["inflación", "costos", "divisas", "dólar", "tasas",
                         "aranceles", "aduanas", "recesión", "deuda", "economía"]
    }
    
    score = 0
    categoria_dominante = "Ninguna"
    max_matches = 0
    
    for categoria, keywords in riesgos.items():
        matches = 0
        for kw in keywords:
            matches += len(re.findall(r'\b' + kw + r'\b', texto))
        
        # Ponderación de score
        score += matches * 2
        
        if matches > max_matches:
            max_matches = matches
            categoria_dominante = categoria

    if score >= 6:
        nivel = "Alto"
    elif score >= 2:
        nivel = "Medio"
    else:
        nivel = "Bajo"
        
    return nivel, score, categoria_dominante


def ejecutar_transformacion():
    """Ejecuta el pipeline completo de transformación y enriquecimiento."""
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
            df_noticias = pd.read_sql("SELECT * FROM noticias_mercado", conn)
            
            if df_noticias.empty:
                print("[-] No hay noticias para procesar. Ejecuta primero el scrapper.")
                return

            print(f"[*] {len(df_noticias)} noticias leídas. Aplicando modelo NLP...")
            
            # Aplicar transformación NLP a cada noticia
            resultados = df_noticias['texto_completo'].apply(aplicar_nlp_basico)
            df_noticias['nivel_riesgo'] = [r[0] for r in resultados]
            df_noticias['score_riesgo'] = [r[1] for r in resultados]
            df_noticias['categoria_riesgo'] = [r[2] for r in resultados]

            # Seleccionar columnas para la tabla enriquecida
            columnas_disponibles = df_noticias.columns.tolist()
            columnas_deseadas = ['titulo', 'fecha_publicacion', 'temas_relacionados',
                                 'nivel_riesgo', 'score_riesgo', 'categoria_riesgo', 'url']
            columnas_finales = [c for c in columnas_deseadas if c in columnas_disponibles]
            df_enriquecido = df_noticias[columnas_finales].copy()
            
            print("[*] Guardando tabla 'noticias_enriquecidas' en PostgreSQL...")
            # PostgreSQL no permite hacer DROP a una tabla (lo que hace to_sql con if_exists='replace') si una vista depende de ella.
            conn.execute(text("DROP VIEW IF EXISTS vw_riesgo_logistico;"))
            conn.commit()
            df_enriquecido.to_sql("noticias_enriquecidas", engine, if_exists='replace', index=False)
            
            # Resumen de distribución de riesgos
            distribucion = df_enriquecido['nivel_riesgo'].value_counts()
            print(f"[+] Éxito: {len(df_enriquecido)} noticias enriquecidas guardadas.")
            print(f"    Distribución -> Alto: {distribucion.get('Alto', 0)} | "
                  f"Medio: {distribucion.get('Medio', 0)} | Bajo: {distribucion.get('Bajo', 0)}")
            
            # Crear Vista Analítica para Power BI
            print("[*] Creando Vista Analítica (vw_riesgo_logistico) para Power BI...")
            vista_sql = text("""
            CREATE OR REPLACE VIEW vw_riesgo_logistico AS
            SELECT 
                n.titulo,
                n.nivel_riesgo,
                n.score_riesgo,
                n.categoria_riesgo,
                n.temas_relacionados,
                n.url,
                CURRENT_DATE AS fecha_analisis
            FROM noticias_enriquecidas n
            ORDER BY n.score_riesgo DESC;
            """)
            conn.execute(vista_sql)
            conn.commit()
            print("[+] Vista SQL 'vw_riesgo_logistico' creada exitosamente.")
            
    except Exception as e:
        print(f"[ERROR CRÍTICO] Fallo en la transformación: {e}")


if __name__ == "__main__":
    ejecutar_transformacion()
