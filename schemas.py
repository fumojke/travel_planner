from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

# ==========================================
# (PLACES)
# ==========================================

class PlaceBase(BaseModel):
    external_id: str
    notes: Optional[str] = None
    is_visited: bool = False

class PlaceCreate(PlaceBase):
    pass

class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None

class PlaceResponse(PlaceBase):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# (TRAVEL PROJECTS)
# ==========================================

class TravelProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None

class TravelProjectCreate(TravelProjectBase):
    places: Optional[List[PlaceCreate]] = []

class TravelProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None

class TravelProjectResponse(TravelProjectBase):
    id: int
    is_completed: bool
    places: List[PlaceResponse] = []

    model_config = ConfigDict(from_attributes=True)