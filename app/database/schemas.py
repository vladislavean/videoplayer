import uuid

from pydantic import BaseModel


class SchemaStreet(BaseModel):
    id: uuid.UUID
    name: str


class SchemaCamera(BaseModel):
    id: uuid.UUID
    title: str
    streetId: uuid.UUID
    address: str


class SchemaArchiveTask(BaseModel):
    id: uuid.UUID
    url: str
    cameraId: uuid.UUID


class SchemaUsers(BaseModel):
    id: uuid.UUID
    login: str
    fio: str
    roleId: uuid.UUID
    password: str


class SchemaFunctionalRoles(BaseModel):
    id: uuid.UUID
    name: str
