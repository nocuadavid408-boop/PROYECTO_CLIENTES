from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class ClienteBase(SQLModel):
    nombre: str
    edad: int
    descripcion: Optional[str] = None


class ClienteCrear(ClienteBase):
    pass


class ClienteActualizar(SQLModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
    descripcion: Optional[str] = None


class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    facturas: List["Factura"] = Relationship(back_populates="cliente")


class ClienteLeer(ClienteBase):
    id: int


class ClienteLeerCompuesto(ClienteLeer):
    facturas: List["FacturaLeer"] = []


from app.models.facturas import Factura, FacturaLeer  

ClienteLeerCompuesto.model_rebuild()

