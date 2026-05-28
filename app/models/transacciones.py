from pydantic import BaseModel

from app.models.facturas import Factura


class TransaccionCrear(BaseModel):
    descripcion: str
    factura: Factura


class Transaccion(TransaccionCrear):
    id: int