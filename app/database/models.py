from datetime import datetime
from typing import Optional, Annotated
import uuid
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


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


class Streets(Base):
    __tablename__ = 'streets'

    id: Mapped[uuid_pk]
    name: Mapped[str]


class Cameras(Base):
    __tablename__ = 'cameras'

    id: Mapped[uuid_pk]
    title: Mapped[str]
    streetId: Mapped[uuid_pk] = mapped_column(ForeignKey("streets.id"))
    address: Mapped[str]


class ArchivesTask(Base):
    __tablename__ = 'archivestask'

    id: Mapped[uuid_pk]
    cameraId = mapped_column(ForeignKey("cameras.id"))
