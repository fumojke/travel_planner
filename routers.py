from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/projects",
    tags=["Travel Projects"]
)


@router.post("/", response_model=schemas.TravelProjectResponse)
def create_project(project: schemas.TravelProjectCreate, db: Session = Depends(get_db)):
    db_project = models.TravelProject(
        name=project.name,
        description=project.description,
        start_date=project.start_date
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


@router.get("/", response_model=List[schemas.TravelProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.TravelProject).all()
    return projects


@router.get("/{project_id}", response_model=schemas.TravelProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).filter(models.TravelProject.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).filter(models.TravelProject.id == project_id).first()

    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    for place in project.places:
        if place.is_visited:
            raise HTTPException(status_code=400, detail="Cannot delete project with visited places")

    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}