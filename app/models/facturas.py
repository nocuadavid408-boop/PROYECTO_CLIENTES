from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Factura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.now)
    cliente_id: int


class FacturaCrear(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)
    cliente_id: int


class Transaccion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    valor_unitario: float
    cantidad: int
    factura_id: int


class TransaccionCrear(SQLModel):
    valor_unitario: float
    cantidad: int
    factura_id: int
