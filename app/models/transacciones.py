from typing import Optional
from sqlmodel import SQLModel

# La tabla Transaccion vive en app/models/facturas.py (es la que usan los
# routers). Este archivo NO debe volver a declarar table=True para
# "transaccion" o SQLAlchemy lanzará un error de tabla duplicada.
from app.models.facturas import Transaccion, TransaccionCrear  # noqa: F401


class TransaccionActualizar(SQLModel):
    valor_unitario: Optional[float] = None
    cantidad: Optional[int] = None
    factura_id: Optional[int] = None


class TransaccionLeer(SQLModel):
    id: int
    valor_unitario: float
    cantidad: int
    factura_id: int
