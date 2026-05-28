from pydantic import BaseModel
from datetime import datetime

from app.models.clientes import Cliente


class FacturaCrear(BaseModel):
    fecha: datetime = datetime.now()
    cliente: Cliente
    valortotal: float


class Factura(FacturaCrear):
    id: int