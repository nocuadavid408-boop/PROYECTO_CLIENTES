from typing import Optional
from sqlmodel import SQLModel, Field


class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    descripcion: Optional[str] = None


class ClienteCrear(SQLModel):
    nombre: str
    edad: int
    descripcion: Optional[str] = None
