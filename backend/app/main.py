"""Aplicación FastAPI: algoritmo genético de aproximación de imágenes con triángulos."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .api import router as api_router
from .ws import router as ws_router

app = FastAPI(title="AG Triángulos")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
app.include_router(ws_router)
