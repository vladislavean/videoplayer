from datetime import datetime
from pydantic import BaseModel


class Recording(BaseModel):
    date: datetime
    link: str


class Street(BaseModel):
    name: str
    recordings: list[Recording]


class City(BaseModel):
    name: str
    streets: list[Street]
