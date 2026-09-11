import os
import sys
from pathlib import Path

# Add api directory to sys.path so modules resolve cleanly
API_DIR = Path(__file__).resolve().parent
if str(API_DIR) not in sys.path:
    sys.path.insert(0, str(API_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_db
from seed_data import seed_database
from routes.routes_dashboard import router as dashboard_router
from routes.routes_theory import router as theory_router
from routes.routes_practice import router as practice_router
from routes.routes_cases import router as cases_router
from routes.routes_exam import router as exam_router
from routes.routes_errors import router as errors_router
from routes.routes_search import router as search_router
from routes.routes_admin import router as admin_router

app = FastAPI(
    title="Plataforma de Estudio y Práctica — Ingeniería de Datos I",
    description="API Serverless para práctica adaptativa, casos prácticos y simulador de examen.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(theory_router)
app.include_router(practice_router)
app.include_router(cases_router)
app.include_router(exam_router)
app.include_router(errors_router)
app.include_router(search_router)
app.include_router(admin_router)

@app.on_event("startup")
def on_startup():
    init_db()
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM concepts;")
            count = cursor.fetchone()[0]
            if count == 0:
                seed_database()
    except Exception as e:
        print(f"Startup DB check error: {e}")

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "environment": "vercel" if os.environ.get("VERCEL") else "local",
        "units": 6
    }

# Local static serving fallback when run standalone (outside Vercel)
DIST_DIR = API_DIR.parent / "dist"
if DIST_DIR.exists() and not os.environ.get("VERCEL"):
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse
    if (DIST_DIR / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend_spa(full_path: str):
        file_path = DIST_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(DIST_DIR / "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="127.0.0.1", port=8000, reload=True)
