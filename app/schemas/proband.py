from pydantic import BaseModel
from datetime import date
from typing import Optional

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
    isactive: bool

class ProbandCreate(ProbandBase):
    pass

class Proband(ProbandBase):
    id: int

    class Config:
        orm_mode = True