from typing import Optional, Annotated
import uuid
from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


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

    cameras: Mapped[list["Cameras"]] = relationship("Cameras", back_populates="streets")


class Cameras(Base):
    __tablename__ = 'cameras'

    id: Mapped[uuid_pk]
    title: Mapped[str]
    streetId: Mapped[uuid.UUID] = mapped_column(ForeignKey("streets.id"))
    address: Mapped[str]

    street: Mapped["Streets"] = relationship(back_populates="cameras")

    cameras: Mapped[list["ArchivesTask"]] = relationship("ArchivesTask", back_populates="Cameras")


class ArchivesTask(Base):
    __tablename__ = 'archivestask'

    id: Mapped[uuid_pk]
    cameraId: Mapped[uuid.UUID] = mapped_column(ForeignKey("cameras.id"))
    url: Mapped[str]

    street: Mapped["Cameras"] = relationship(back_populates="ArchivesTask")


class FunctionalRoles(Base):
    __tablename__ = "functionalroles"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    users_role: Mapped[list["Users"]] = relationship("Users", back_populates="functional_roles")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid_pk]
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    fio: Mapped[str] = mapped_column(unique=True, nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("functionalroles.id"), name="roleid")
    password: Mapped[str] = mapped_column(nullable=False)

    functional_roles: Mapped["FunctionalRoles"] = relationship(back_populates="users_role")
