from fastapi import APIRouter, HTTPException

from app.models.transacciones import Transaccion, TransaccionCrear
from app.database import lista_transacciones, lista_facturas

router_transacciones = APIRouter()


@router_transacciones.get("/transacciones")
def listar_transacciones():
    return lista_transacciones


@router_transacciones.get("/transacciones/{id}")
def obtener_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")


@router_transacciones.post("/transacciones")
def crear_transaccion(datos: TransaccionCrear):
    factura_existe = any(f.id == datos.factura_id for f in lista_facturas)
    if not factura_existe:
        raise HTTPException(status_code=404, detail=f"No existe una factura con id {datos.factura_id}")
    nueva_id = len(lista_transacciones) + 1
    transaccion = Transaccion(id=nueva_id, **datos.model_dump())
    lista_transacciones.append(transaccion)
    return {"mensaje": "Transacción creada", "transaccion": transaccion}


@router_transacciones.put("/transacciones/{id}")
def editar_transaccion(id: int, datos: TransaccionCrear):
    factura_existe = any(f.id == datos.factura_id for f in lista_facturas)
    if not factura_existe:
        raise HTTPException(status_code=404, detail=f"No existe una factura con id {datos.factura_id}")
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            transaccion.valor_unitario = datos.valor_unitario
            transaccion.cantidad = datos.cantidad
            transaccion.factura_id = datos.factura_id
            return {"mensaje": "Transacción actualizada", "transaccion": transaccion}
    raise HTTPException(status_code=404, detail="Transacción no encontrada")


@router_transacciones.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    for index, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            lista_transacciones.pop(index)
            return {"mensaje": "Transacción eliminada"}
    raise HTTPException(status_code=404, detail="Transacción no encontrada")
