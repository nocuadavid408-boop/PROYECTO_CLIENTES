from pydantic import computed_field
from sqlmodel import SQLModel, Field, Relationship
from .cliente import Cliente, ClienteLeer
from .transacciones import Transaccion
from datetime import datetime


class FacturaBase(SQLModel):
    fecha: datetime = Field(default_factory=datetime.now)


class CrearFactura(FacturaBase):
    pass


class ActualizarFactura(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")

    cliente: Cliente = Relationship(back_populates="facturas")
    transacciones: list["Transaccion"] = Relationship(back_populates="factura")


class FacturaLeer(FacturaBase):
    id: int
    cliente: ClienteLeer | None = None

    @computed_field
    @property
    def valor_total(self) -> float:
        transacciones = getattr(self, "transacciones", None)

        if not transacciones:
            return 0.0

        total_factura = 0.0
        for transaccion in transacciones:
            total_factura += (
                transaccion.valor_unitario * transaccion.cantidad
            )

        return total_factura


class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list["Transaccion"] = []