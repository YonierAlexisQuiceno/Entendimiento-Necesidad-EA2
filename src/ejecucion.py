import os
import sys
import datetime

# Importar los módulos del pipeline
try:
    from scraper import BBCMundoScraperPOO
    from modelo import ejecutar_transformacion
except ImportError:
    print("[ERROR] No se encontraron los archivos scraper.py o modelo.py en la misma ruta.")
    sys.exit(1)

def main():
    log_file = "auditoria.txt"
    with open(log_file, "a", encoding="utf-8") as f:
        inicio = datetime.datetime.now()
        f.write(f"======================================================\n")
        f.write(f"[*] INICIO DE EJECUCIÓN DEL PIPELINE (EA3)\n")
        f.write(f"[*] FECHA Y HORA: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"======================================================\n\n")

        print("\n--- PASO 1: EJECUTANDO SCRAPER (EXTRAER DATOS CRUDOS) ---")
        f.write("[LOG] Iniciando Scraper BBC Mundo...\n")
        try:
            scraper = BBCMundoScraperPOO()
            scraper.ejecutar_pipeline()
            f.write("[LOG] Scraper ejecutado exitosamente.\n")
        except Exception as e:
            f.write(f"[ERROR] Fallo en Scraper: {e}\n")
            print(f"[ERROR] {e}")

        print("\n--- PASO 2: EJECUTANDO MODELO (TRANSFORMACIÓN Y ENRIQUECIMIENTO) ---")
        f.write("[LOG] Iniciando Transformación NLP (modelo.py)...\n")
        try:
            ejecutar_transformacion()
            f.write("[LOG] Transformación de datos ejecutada exitosamente.\n")
        except Exception as e:
            f.write(f"[ERROR] Fallo en Modelo: {e}\n")
            print(f"[ERROR] {e}")

        fin = datetime.datetime.now()
        f.write(f"\n[*] FIN DE EJECUCIÓN. DURACIÓN: {(fin - inicio).total_seconds()} segundos.\n")
        f.write(f"======================================================\n\n")
    
    print(f"\n[OK] Pipeline finalizado. Revisa el archivo '{log_file}' para la auditoría.")

if __name__ == "__main__":
    main()
