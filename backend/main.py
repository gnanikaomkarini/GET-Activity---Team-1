from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from .database import engine, Base
from .routers import devices_router, readings_router, simulation_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Energy Efficiency Advisor",
    description="AI-powered energy simulation and recommendations",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices_router)
app.include_router(readings_router)
app.include_router(simulation_router)

if os.path.exists("../frontend"):
    app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
