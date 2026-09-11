#!/usr/bin/env python3
"""
Launcher maestro para la Plataforma de Estudio y Práctica — Base de Datos I.
Verifica dependencias, base de datos SQLite, empaquetado frontend e inicia el servidor web local.
"""

import os
import sys
import time
import webbrowser
import threading
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
API_DIR = BASE_DIR / "api"
DIST_DIR = BASE_DIR / "dist"
DB_PATH = API_DIR / "plataforma.db"

def check_environment():
    print("=================================================================")
    print("   PLATAFORMA INTEGRAL DE ESTUDIO Y PRÁCTICA — BASE DE DATOS I   ")
    print("=================================================================")
    print(f"Directorio base: {BASE_DIR}")

    # Check python packages
    try:
        import fastapi
        import uvicorn
        print("✓ Dependencias FastAPI y Uvicorn detectadas.")
    except ImportError:
        print("Instalando dependencias de Python necesarias...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"])

    # Check database
    if not DB_PATH.exists():
        print("Base de datos no encontrada. Inicializando y sembrando contenido curricular...")
        sys.path.insert(0, str(API_DIR))
        from database import init_db
        from seed_data import seed_database
        init_db()
        seed_database()
        print("✓ Base de datos sembrada con las 5 presentaciones oficiales de cátedra.")
    else:
        print(f"✓ Base de datos SQLite lista: {DB_PATH.name}")

    # Check frontend dist
    if not (DIST_DIR / "index.html").exists():
        print("Compilando el frontend de la plataforma (Vite + React + Tailwind)...")
        import subprocess
        subprocess.check_call(["npm", "run", "build"], cwd=str(BASE_DIR), shell=True)
        print("✓ Frontend compilado exitosamente.")
    else:
        print("✓ Interfaz React compilada disponible en dist/.")

def open_browser():
    time.sleep(1.5)
    url = "http://localhost:8000"
    print(f"\n🚀 Abriendo navegador en {url}...")
    webbrowser.open(url)

def main():
    check_environment()
    
    # Run browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Run FastAPI server with Uvicorn
    print("\nIniciando servidor web...")
    print("Presioná CTRL+C para detener el servidor.\n")
    
    import uvicorn
    sys.path.insert(0, str(API_DIR))
    from index import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    main()
