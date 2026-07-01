from pydantic import BaseModel


class TransaccionCrear(BaseModel):
    valor_unitario: float
    cantidad: int
    factura_id: int


class Transaccion(TransaccionCrear):
    id: int
