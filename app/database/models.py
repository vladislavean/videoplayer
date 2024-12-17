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
    __tablename__ = "streets"

    id: Mapped[uuid_pk]
    name: Mapped[str]

    cameras: Mapped[list["Cameras"]] = relationship("Cameras", back_populates="street")


# Камеры
class Cameras(Base):
    __tablename__ = "cameras"

    id: Mapped[uuid_pk]
    title: Mapped[str]
    streetId: Mapped[uuid.UUID] = mapped_column(ForeignKey("streets.id"))
    address: Mapped[str]

    street: Mapped["Streets"] = relationship(back_populates="cameras")
    archives: Mapped[list["ArchivesTask"]] = relationship("ArchivesTask", back_populates="camera")


# Архивные задачи
class ArchivesTask(Base):
    __tablename__ = "archivestask"

    id: Mapped[uuid_pk]
    name: Mapped[str]
    cameraId: Mapped[uuid.UUID] = mapped_column(ForeignKey("cameras.id"))
    url: Mapped[str]

    camera: Mapped["Cameras"] = relationship(back_populates="archives")


# Функциональные роли
class FunctionalRoles(Base):
    __tablename__ = "functionalroles"

    id: Mapped[uuid_pk]
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[list["Users"]] = relationship("Users", back_populates="functional_role")


# Пользователи
class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid_pk]
    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    fio: Mapped[str] = mapped_column(unique=True, nullable=False)
    roleId: Mapped[uuid.UUID] = mapped_column(ForeignKey("functionalroles.id"))
    password: Mapped[str] = mapped_column(nullable=False)

    functional_role: Mapped["FunctionalRoles"] = relationship(back_populates="users")
