from pydantic import BaseModel
from datetime import datetime
from typing import List


class TransaccionCrear(BaseModel):
    valor_unitario: float
    cantidad: int
    factura_id: int


class Transaccion(TransaccionCrear):
    id: int


class FacturaCrear(BaseModel):
    fecha: datetime = datetime.now()
    cliente_id: int


class Factura(FacturaCrear):
    id: int

    def valor_total(self, lista_transacciones: list) -> float:
        total = 0.0
        for t in lista_transacciones:
            if t.factura_id == self.id:
                total += t.valor_unitario * t.cantidad
        return total
