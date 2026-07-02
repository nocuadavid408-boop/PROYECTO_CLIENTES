from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.facturas import Factura


# MODELO BASE
class TransaccionBase(SQLModel):
    descripcion: str

    valor_unitario: float

    cantidad: int

    factura_id: int = Field(
        foreign_key="facturas.id"
    )


# CREAR TRANSACCION
class TransaccionCrear(TransaccionBase):
    pass


# ACTUALIZAR TRANSACCION
class TransaccionActualizar(SQLModel):
    descripcion: Optional[str] = None

    valor_unitario: Optional[float] = None

    cantidad: Optional[int] = None


# TABLA TRANSACCION

class Transaccion(
    TransaccionBase,
    table=True
):
    __tablename__ = "transacciones"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    # relación con factura
    factura: "Factura" = Relationship(
        back_populates="transacciones"
    )

    # subtotal
    @property
    def subtotal(self):
        return (
            self.valor_unitario *
            self.cantidad
        )


class TransaccionPublica(SQLModel):
    id: int

    descripcion: str

    valor_unitario: float

    cantidad: int

    factura_id: int

    subtotal: float


class TransaccionDetalle(SQLModel):
    id: int
    descripcion: str
    valor_unitario: float
    cantidad: int
    subtotal: float
    factura: dict
    cliente: dict
    valor_total_factura: float