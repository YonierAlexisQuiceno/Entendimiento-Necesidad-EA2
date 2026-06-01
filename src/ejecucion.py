"""
Orquestador del Pipeline Completo (EA3)
Autor: Yonier Alexis Quiceno Rodríguez
Descripción: Ejecuta secuencialmente el scrapper y el modelo de enriquecimiento,
registrando toda la actividad en el archivo auditoria.txt.
"""

import os
import sys
import datetime

# Asegurar que el directorio src está en el PATH de importación
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar los módulos del pipeline
try:
    from scrapper import BBCMundoScraperPOO
    from modelo import ejecutar_transformacion
except ImportError as e:
    print(f"[ERROR] No se pudieron importar los módulos del pipeline: {e}")
    sys.exit(1)


def main():
    log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "auditoria.txt")
    log_file = os.path.normpath(log_file)

    with open(log_file, "a", encoding="utf-8") as f:
        inicio = datetime.datetime.now()
        f.write(f"======================================================\n")
        f.write(f"[*] INICIO DE EJECUCIÓN DEL PIPELINE (EA3)\n")
        f.write(f"[*] FECHA Y HORA: {inicio.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"======================================================\n\n")

        print("\n--- PASO 1: EJECUTANDO SCRAPPER (EXTRAER DATOS CRUDOS) ---")
        f.write("[LOG] Iniciando Scrapper BBC Mundo...\n")
        try:
            scraper = BBCMundoScraperPOO()
            scraper.ejecutar_pipeline()
            f.write("[LOG] Scrapper ejecutado exitosamente.\n")
        except Exception as e:
            f.write(f"[ERROR] Fallo en Scrapper: {e}\n")
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
        duracion = (fin - inicio).total_seconds()
        f.write(f"\n[*] FIN DE EJECUCIÓN. DURACIÓN: {duracion:.1f} segundos.\n")
        f.write(f"======================================================\n\n")
    
    print(f"\n[OK] Pipeline finalizado. Revisa el archivo '{log_file}' para la auditoría.")


if __name__ == "__main__":
    main()
