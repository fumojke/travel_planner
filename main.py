from fastapi import FastAPI
import models
from database import engine

from routers import router as projects_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Travel Planner API",
    description="API for planning trips and saving places to visit",
    version="1.0.0"
)

app.include_router(projects_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel Planner API 2.0!"}