from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.models.facturas import Transaccion, TransaccionCrear, Factura
from app.conexion_bd import get_session

rutas_transacciones = APIRouter(tags=["transacciones"])


@rutas_transacciones.get("/transacciones", tags=["transacciones"])
def listar_transacciones(session: Session = Depends(get_session)):
    return session.exec(select(Transaccion)).all()


@rutas_transacciones.get("/transacciones/{id}", tags=["transacciones"])
def obtener_transaccion(id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion


@rutas_transacciones.post("/facturas/{factura_id}/transacciones", tags=["transacciones"])
def crear_transaccion(
    factura_id: int,
    datos: TransaccionCrear,
    session: Session = Depends(get_session)
):
    factura = session.get(Factura, factura_id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail=f"No existe una factura con id {factura_id}"
        )

    transaccion = Transaccion(
        valor_unitario=datos.valor_unitario,
        cantidad=datos.cantidad,
        factura_id=factura_id
    )

    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)

    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion
    }


@rutas_transacciones.put("/transacciones/{id}", tags=["transacciones"])
def editar_transaccion(id: int, datos: TransaccionCrear, session: Session = Depends(get_session)):
    factura = session.get(Factura, datos.factura_id)
    if not factura:
        raise HTTPException(status_code=404, detail=f"No existe una factura con id {datos.factura_id}")
    transaccion = session.get(Transaccion, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    transaccion.valor_unitario = datos.valor_unitario
    transaccion.cantidad = datos.cantidad
    transaccion.factura_id = datos.factura_id
    session.commit()
    session.refresh(transaccion)
    return {"mensaje": "Transacción actualizada", "transaccion": transaccion}


@rutas_transacciones.delete("/transacciones/{id}", tags=["transacciones"])
def eliminar_transaccion(id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, id)
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    session.delete(transaccion)
    session.commit()
    return {"mensaje": "Transacción eliminada"}