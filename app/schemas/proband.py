from pydantic import BaseModel
from datetime import date
from uuid import UUID


class ProbandBase(BaseModel):
    firstname: str
    lastname: str
    email: str
    gender_id: int
    birthday: date
    weight: float
    height: float
    health: float
    country_id: int
    isActive: bool
    lastChanged: date


class ProbandCreate(ProbandBase):
    pass


class Proband(ProbandBase):
    id: UUID

    class Config:
        from_attributes = True
