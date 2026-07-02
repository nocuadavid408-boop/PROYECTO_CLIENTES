from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.facturas import Factura


# MODELO BASE
class ClienteBase(SQLModel):
    nombre: str
    edad: int
    descripcion: Optional[str] = None


# CREAR CLIENTE
class ClienteCrear(ClienteBase):
    pass

# ACTUALIZAR CLIENTE
class ClienteActualizar(SQLModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
    descripcion: Optional[str] = None


# TABLA CLIENTES
class Cliente(ClienteBase, table=True):
    __tablename__ = "clientes"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    # Relación con facturas
    facturas: list["Factura"] = Relationship(
        back_populates="cliente"
    )


# RESPUESTA PÚBLICA
class ClientePublico(ClienteBase):
    id: int

# CLIENTE CON FACTURAS
class ClienteDetalle(SQLModel):
    id: int
    nombre: str
    edad: int
    descripcion: Optional[str]

    facturas: list = []