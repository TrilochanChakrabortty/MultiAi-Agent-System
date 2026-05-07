from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.api.v1.endpoints import query, upload
from app.core.config import settings
from app.core.logger import logger
from app.core.database import engine, Base
from app.models import db_models

app = FastAPI()

# 🔥 DB SETUP (REMOVE drop_all in production later)
Base.metadata.create_all(bind=engine)

# -----------------------------
# STATIC FILES
# -----------------------------
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# -----------------------------
# SERVE UI
# -----------------------------
@app.get("/")
async def serve_ui():
    return FileResponse("app/static/index.html")

# -----------------------------
# API ROUTES
# -----------------------------
app.include_router(query.router, prefix="/api/v1")
app.include_router(upload.router, prefix="/api/v1")

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
async def health_check():
    return {"status": "healthy"}