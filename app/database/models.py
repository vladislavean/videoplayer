from datetime import datetime
from typing import Optional, Annotated
import uuid
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase


uuid_pk = Annotated[
    uuid.UUID,
    mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True,
    ),
]


class Base(DeclarativeBase):
    id: Mapped[uuid_pk]


# class Street(Base):
#     name: str
#
#
# class Cameras(Base):
#     title: str
#     district: str
#
#
#
# class Recording(Base):
#     date: datetime
#     link: str
#
#
# class City(Base):
#     name: str
#     streets: list[Street]
