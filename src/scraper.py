"""
S30 - Entrega 2: Scraper POO Integrado con PostgreSQL y preparado para GCP.
Autor: Yonier Alexis Quiceno Rodríguez
Descripción: Este script extrae noticias de BBC Mundo y las ingiere en una base
de datos PostgreSQL validando duplicados. Diseñado para ejecutarse en Cloud Run.
"""

import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env local
load_dotenv()

class BBCMundoScraperPOO:
    def __init__(self):
        """Inicializa configuración del scraper y conexión a PostgreSQL."""
        self.base_url = "https://www.bbc.com"
        self.topic_url = f"{self.base_url}/mundo/topics/c7zp57yyz25t"

        # Headers para evitar bloqueo (Error 403)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        }

        # Conexión a PostgreSQL vía SQLAlchemy usando variables de entorno
        db_user = os.getenv("DB_USER", "postgres")
        db_pass = os.getenv("DB_PASSWORD", "admin")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "shopanalytics")

        self.db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(self.db_url)

    def obtener_sopa(self, url):
        """Realiza la petición HTTP y retorna un objeto BeautifulSoup."""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.text, "lxml")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Fallo al acceder a {url}: {e}")
            return None

    def extraer_listado_noticias(self):
        """Extrae la metadata básica de la página de inicio del topic."""
        print(f"[*] Escaneando listado de noticias en: {self.topic_url}")
        soup = self.obtener_sopa(self.topic_url)
        if not soup:
            return []

        noticias = []
        # Buscar tarjetas con el tag data-testid="promo"
        promos = soup.find_all("div", attrs={"data-testid": lambda value: value and "promo" in value})

        # Fallback por si la estructura cambia
        if not promos:
            promos = soup.find_all(["article", "div"], class_=lambda c: c and "promo" in c)

        print(f"[*] Se encontraron {len(promos)} tarjetas de noticias.")

        for promo in promos:
            noticia = {}

            titulo_tag = promo.find(["h2", "h3"])
            noticia["titulo"] = titulo_tag.get_text(strip=True) if titulo_tag else None

            desc_tag = promo.find("p")
            noticia["descripcion"] = desc_tag.get_text(strip=True) if desc_tag else "Sin descripción"

            time_tag = promo.find("time")
            noticia["fecha_publicacion"] = time_tag.get_text(strip=True) if time_tag else "Fecha desconocida"

            link_tag = promo.find("a", href=True)
            if link_tag:
                href = link_tag["href"]
                noticia["url"] = self.base_url + href if href.startswith("/") else href
            else:
                noticia["url"] = None

            if noticia["titulo"] and noticia["url"]:
                noticias.append(noticia)

        return noticias

    def extraer_cuerpo_articulo(self, url):
        """Navega a la URL específica y extrae el texto completo para NLP/SVM."""
        soup = self.obtener_sopa(url)
        if not soup:
            return "", ""

        # Extraer texto del artículo
        bloques = soup.find_all(attrs={"data-component": "text-block"})
        if not bloques:
            contenedor = soup.find("main") or soup.find("article")
            bloques = contenedor.find_all("p") if contenedor else []

        texto_completo = "\n".join(b.get_text(strip=True) for b in bloques)

        # Extraer etiquetas (Tags)
        temas = []
        temas_links = soup.find_all("a", class_=lambda c: c and ("topic" in c or "tag" in c))
        for t in temas_links:
            tema_txt = t.get_text(strip=True)
            if tema_txt not in temas:
                temas.append(tema_txt)

        return texto_completo, ", ".join(temas)

    def guardar_en_postgres(self, df_nuevas, tabla="noticias_mercado"):
        """Ingesta el DataFrame en PostgreSQL evitando duplicidad de URLs."""
        try:
            # Comprobar si la tabla existe y traer URLs previas
            with self.engine.connect() as conn:
                try:
                    df_existentes = pd.read_sql(f"SELECT url FROM {tabla}", conn)
                    urls_existentes = set(df_existentes['url'].tolist())
                except Exception:
                    # Si la tabla no existe, falla la consulta, asumimos 0 URLs existentes
                    urls_existentes = set()

            # Filtrar DataFrame dejando solo noticias que NO están en la BD
            df_a_insertar = df_nuevas[~df_nuevas['url'].isin(urls_existentes)]
            duplicados = len(df_nuevas) - len(df_a_insertar)

            if duplicados > 0:
                print(f"[*] Limpieza: {duplicados} noticias ignoradas (Ya existen en PostgreSQL).")

            if not df_a_insertar.empty:
                # Inserción en PostgreSQL
                df_a_insertar.to_sql(tabla, self.engine, if_exists='append', index=False)
                print(f"[+] ÉXITO: {len(df_a_insertar)} nuevos registros insertados en la tabla '{tabla}'.")
            else:
                print("[-] No hay noticias nuevas para ingestar en este momento.")

        except Exception as e:
            print(f"[ERROR CRÍTICO] Fallo en la conexión/inserción a PostgreSQL: {e}")

    def ejecutar_pipeline(self):
        """Método principal que orquesta todo el flujo ETL."""
        print("="*60)
        print(" INICIANDO PIPELINE DE SCRAPING - SHOPANALYTICS S.A.S.")
        print("="*60)

        lista_basica = self.extraer_listado_noticias()

        print("\n[*] Extrayendo detalle de artículos (Preparación para modelo SVM)...")
        for i, noticia in enumerate(lista_basica):
            print(f"  [{i+1}/{len(lista_basica)}] Procesando: {noticia['titulo'][:40]}...")
            texto, temas = self.extraer_cuerpo_articulo(noticia["url"])
            noticia["texto_completo"] = texto
            noticia["temas_relacionados"] = temas
            time.sleep(1.5)  # Respetar rate limiting (Pausa Ética)

        # Transformar a Pandas DataFrame
        df_final = pd.DataFrame(lista_basica)

        # Conectar e Ingestar en PostgreSQL
        print("\n[*] Conectando a PostgreSQL para ingesta de datos...")
        self.guardar_en_postgres(df_final)

        print("="*60)
        print(" PIPELINE FINALIZADO CON ÉXITO")
        print("="*60)

if __name__ == "__main__":
    # Instanciar el objeto y ejecutar
    scraper = BBCMundoScraperPOO()
    scraper.ejecutar_pipeline()