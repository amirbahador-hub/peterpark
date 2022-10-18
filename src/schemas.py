from pydantic import BaseModel, Field
from typing import Optional


class Search(BaseModel):
    key: str
    levenshtein: Optional[int] = 0


class PlateInput(BaseModel):
    raw_plate: str = Field(alias="plate")
