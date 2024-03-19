from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class GenderBase(BaseModel):
    name: str


class GenderCreate(GenderBase):
    pass


class Gender(GenderBase):
    id: UUID

    class Config:
        orm_mode = True
