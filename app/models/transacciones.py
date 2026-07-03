from sqlmodel import SQLModel, Field, Relationship


class TransaccionBase(SQLModel):
    cantidad: int = Field(default=0)
    valor_unitario: float = Field(default=0.0)
    descripcion: str | None = Field(default=None)


class CrearTransaccion(TransaccionBase):
    pass


class ModificarTransaccion(TransaccionBase):
    pass


class ActualizarTransaccion(TransaccionBase):
    pass


class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int = Field(foreign_key="factura.id")

    factura: "Factura" = Relationship(back_populates="transacciones")


class TransaccionLeer(TransaccionBase):
    id: int