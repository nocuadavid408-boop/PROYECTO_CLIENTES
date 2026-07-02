from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.clientes import Cliente
    from app.models.transacciones import Transaccion


# MODELO BASE
class FacturaBase(SQLModel):
    cliente_id: int = Field(
        foreign_key="clientes.id"
    )


# CREAR FACTURA
class FacturaCrear(FacturaBase):
    pass


# ACTUALIZAR FACTURA
class FacturaActualizar(SQLModel):
    pass


# TABLA FACTURAS
class Factura(FacturaBase, table=True):
    __tablename__ = "facturas"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    fecha: datetime = Field(
        default_factory=datetime.now
    )

    # Relación con cliente
    cliente: "Cliente" = Relationship(
        back_populates="facturas"
    )

    # Relación con transacciones
    transacciones: list["Transaccion"] = Relationship(
        back_populates="factura"
    )

    # Valor total de la factura
    @property
    def valor_total(self):
        return sum(
            t.valor_unitario * t.cantidad
            for t in self.transacciones
        )


# RESPUESTA SIMPLE
class FacturaPublica(SQLModel):
    id: int
    fecha: datetime
    cliente_id: int


# FACTURA COMPLETA
class FacturaDetalle(SQLModel):
    id: int
    fecha: datetime

    cliente: dict

    transacciones: list

    valor_total: float