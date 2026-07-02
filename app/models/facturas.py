from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.now)
    cliente_id: Optional[int] = Field(default=None, foreign_key="cliente.id")

    cliente: Optional["Cliente"] = Relationship(back_populates="facturas")
    transacciones: List["Transaccion"] = Relationship(back_populates="factura")


class FacturaCrear(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    cliente_id: int


class FacturaLeer(SQLModel):
    id: int
    fecha: datetime
    cliente_id: int


class Transaccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    valor_unitario: float
    cantidad: int
    factura_id: Optional[int] = Field(default=None, foreign_key="factura.id")

    factura: Optional["Factura"] = Relationship(back_populates="transacciones")


class TransaccionCrear(SQLModel):
    valor_unitario: float
    cantidad: int
    factura_id: int


from app.models.clientes import Cliente
