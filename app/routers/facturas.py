from fastapi import APIRouter, HTTPException

from app.models.facturas import Factura, FacturaCrear
from app.database import lista_facturas, lista_transacciones

router_facturas = APIRouter()


@router_facturas.get("/facturas")
def listar_facturas():
    return lista_facturas


@router_facturas.get("/facturas/{id}")
def obtener_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            return factura
    raise HTTPException(status_code=404, detail="Factura no encontrada")


@router_facturas.get("/facturas/{id}/valor_total")
def obtener_valor_total(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            total = factura.valor_total(lista_transacciones)
            return {"factura_id": id, "valor_total": total}
    raise HTTPException(status_code=404, detail="Factura no encontrada")


@router_facturas.post("/facturas")
def crear_factura(datos: FacturaCrear):
    nueva_id = len(lista_facturas) + 1
    factura = Factura(id=nueva_id, **datos.model_dump())
    lista_facturas.append(factura)
    return {"mensaje": "Factura creada", "factura": factura}


@router_facturas.put("/facturas/{id}")
def editar_factura(id: int, datos: FacturaCrear):
    for factura in lista_facturas:
        if factura.id == id:
            factura.fecha = datos.fecha
            factura.cliente_id = datos.cliente_id
            return {"mensaje": "Factura actualizada", "factura": factura}
    raise HTTPException(status_code=404, detail="Factura no encontrada")


@router_facturas.delete("/facturas/{id}")
def eliminar_factura(id: int):
    for index, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas.pop(index)
            return {"mensaje": "Factura eliminada"}
    raise HTTPException(status_code=404, detail="Factura no encontrada")
