from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    edad: int
    descripcion: Optional[str] = None

    facturas: List["Factura"] = Relationship(back_populates="cliente")


class ClienteCrear(SQLModel):
    nombre: str
    edad: int
    descripcion: Optional[str] = None
