from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import create_tables
from backend.routes import optimizer, places, routes


app = FastAPI(
    title="Travel Route Optimizer",
    description="Веб-приложение для подбора маршрута путешествия через несколько точек",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    При запуске backend создаёт таблицы базы данных,
    если они ещё не существуют.
    """

    create_tables()


@app.get("/")
def home():
    return {
        "message": "Travel Route Optimizer API работает",
        "status": "ok",
        "architecture": "FastAPI + Repository Pattern + SQLite"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "Travel Route Optimizer",
        "database": "connected"
    }


app.include_router(places.router)
app.include_router(routes.router)
app.include_router(optimizer.router)