from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.staticfiles import StaticFiles

from app.api import user as user_api
from app.api import post as post_api
from app.api import noticia as noticia_api
from app.api import matricula_curso as matricula_api
from app.api import interest as interest_api
from app.api import user_interest as user_interest_api
from app.api import apoio as apoio_api
from app.api import bus_info as bus_info_api
from app.api import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5174", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_api.router, prefix="/users", tags=["users"])
app.include_router(post_api.router, prefix="/posts", tags=["posts"])
app.include_router(noticia_api.router, prefix="/news", tags=["news"])
app.include_router(matricula_api.router, prefix="/enrollments", tags=["matriculas"])
app.include_router(interest_api.router, prefix="/interests", tags=["interests"])
app.include_router(user_interest_api.router, prefix="/user-interests", tags=["user-interests"])
app.include_router(apoio_api.router, prefix="/supports", tags=["apoios"])
app.include_router(bus_info_api.router, prefix="/bus-info", tags=["bus-info"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Serve built frontend (if available) at root
_frontend_dist = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "web-2025-2-lumen-colares-pinho-frontend", "dist")
)
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")
