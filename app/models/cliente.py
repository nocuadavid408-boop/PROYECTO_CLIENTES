from sqlmodel import SQLModel, Field, Relationship

class ClienteBase(SQLModel):
    nombre: str | None = Field(default=None)
    edad: int | None = Field(default=None)
    descripcion: str | None = Field(default=None)

class ClienteCrear(ClienteBase):
    pass

class ClienteActualizar(ClienteBase):
    pass

class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    facturas: list["Factura"] = Relationship(back_populates="cliente")

class ClienteLeer(ClienteBase):
    id: int