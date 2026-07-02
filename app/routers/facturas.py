from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.models.facturas import Factura, FacturaCrear, Transaccion
from app.models.clientes import Cliente
from app.conexion_bd import get_session

rutas_facturas = APIRouter(tags=["facturas"])


@rutas_facturas.get("/facturas/{id}", tags=["facturas"])
def obtener_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)

    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    cliente = session.get(Cliente, factura.cliente_id)

    return {
        "id": factura.id,
        "fecha": factura.fecha,
        "cliente": cliente
    }


@rutas_facturas.get("/facturas/{id}/valor_total", tags=["facturas"])
def obtener_valor_total(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)

    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")

    transacciones = session.exec(
        select(Transaccion).where(Transaccion.factura_id == id)
    ).all()

    total = sum(t.valor_unitario * t.cantidad for t in transacciones)

    return {
        "factura_id": id,
        "valor_total": total
    }


@rutas_facturas.post("/facturas", tags=["facturas"])
def crear_factura(datos: FacturaCrear, session: Session = Depends(get_session)):

    cliente = session.get(Cliente, datos.cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="El cliente no existe"
        )

    factura = Factura(**datos.model_dump())

    session.add(factura)
    session.commit()
    session.refresh(factura)

    return {
        "mensaje": "Factura creada",
        "factura": factura
    }


@rutas_facturas.put("/facturas/{id}", tags=["facturas"])
def editar_factura(id: int, datos: FacturaCrear, session: Session = Depends(get_session)):

    factura = session.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    cliente = session.get(Cliente, datos.cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="El cliente no existe"
        )

    factura.fecha = datos.fecha
    factura.cliente_id = datos.cliente_id

    session.commit()
    session.refresh(factura)

    return {
        "mensaje": "Factura actualizada",
        "factura": factura
    }


@rutas_facturas.delete("/facturas/{id}", tags=["facturas"])
def eliminar_factura(id: int, session: Session = Depends(get_session)):

    factura = session.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    session.delete(factura)
    session.commit()

    return {
        "mensaje": "Factura eliminada"
    }