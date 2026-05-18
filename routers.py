from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import get_db
from services import check_place_exists

# ==========================================
# Projects Router
# ==========================================
router = APIRouter(
    prefix="/projects",
    tags=["Travel Projects"]
)

# 1. CREATE:
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

    if project.places:
        for place_data in project.places:
            if not check_place_exists(place_data.external_id):
                raise HTTPException(status_code=400, detail=f"Place {place_data.external_id} not found in API")

            db_place = models.Place(**place_data.model_dump(), project_id=db_project.id)
            db.add(db_place)

        db.commit()
        db.refresh(db_project)

    return db_project


# 2. READ:
@router.get("/", response_model=List[schemas.TravelProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.TravelProject).all()
    return projects

# 3. READ:
@router.get("/{project_id}", response_model=schemas.TravelProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).filter(models.TravelProject.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

# 4. UPDATE:
@router.patch("/{project_id}", response_model=schemas.TravelProjectResponse)
def update_project(project_id: int, project_update: schemas.TravelProjectUpdate, db: Session = Depends(get_db)):
    db_project = db.query(models.TravelProject).filter(models.TravelProject.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project_update.name is not None:
        db_project.name = project_update.name
    if project_update.description is not None:
        db_project.description = project_update.description
    if project_update.start_date is not None:
        db_project.start_date = project_update.start_date

    db.commit()
    db.refresh(db_project)
    return db_project

# 5. DELETE:
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

# ==========================================
# (PLACES)
# ==========================================

# 6. CREATE:
@router.post("/{project_id}/places", response_model=schemas.PlaceResponse)
def add_place_to_project(project_id: int, place: schemas.PlaceCreate, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).filter(models.TravelProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if len(project.places) >= 10:
        raise HTTPException(status_code=400, detail="A project can have a maximum of 10 places")

    for existing_place in project.places:
        if existing_place.external_id == place.external_id:
            raise HTTPException(status_code=400, detail="This place is already in the project")

    if not check_place_exists(place.external_id):
        raise HTTPException(status_code=404, detail="Place not found in the Art Institute API")

    db_place = models.Place(
        external_id=place.external_id,
        notes=place.notes,
        is_visited=place.is_visited,
        project_id=project_id
    )
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

# 7. UPDATE:
@router.patch("/places/{place_id}", response_model=schemas.PlaceResponse)
def update_place(place_id: int, place_update: schemas.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not db_place:
        raise HTTPException(status_code=404, detail="Place not found")

    if place_update.notes is not None:
        db_place.notes = place_update.notes
    if place_update.is_visited is not None:
        db_place.is_visited = place_update.is_visited

    db.commit()
    db.refresh(db_place)

    project = db_place.project
    all_visited = all(p.is_visited for p in project.places)
    if all_visited and not project.is_completed:
        project.is_completed = True
        db.commit()

    return db_place

# 8. READ:
@router.get("/{project_id}/places", response_model=List[schemas.PlaceResponse])
def get_project_places(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.TravelProject).filter(models.TravelProject.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project.places

# 9. READ:
@router.get("/places/{place_id}", response_model=schemas.PlaceResponse)
def get_single_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(models.Place.id == place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place