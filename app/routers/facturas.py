# rutas o endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.models.facturas import Factura, FacturaCrear, Transaccion
from app.conexion_bd import get_session

rutas_facturas = APIRouter()


@rutas_facturas.get("/facturas")
def listar_facturas(session: Session = Depends(get_session)):
    return session.exec(select(Factura)).all()


@rutas_facturas.get("/facturas/{id}")
def obtener_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@rutas_facturas.get("/facturas/{id}/valor_total")
def obtener_valor_total(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    transacciones = session.exec(select(Transaccion).where(Transaccion.factura_id == id)).all()
    total = sum(t.valor_unitario * t.cantidad for t in transacciones)
    return {"factura_id": id, "valor_total": total}


@rutas_facturas.post("/facturas")
def crear_factura(datos: FacturaCrear, session: Session = Depends(get_session)):
    factura = Factura(**datos.model_dump())
    session.add(factura)
    session.commit()
    session.refresh(factura)
    return {"mensaje": "Factura creada", "factura": factura}


@rutas_facturas.put("/facturas/{id}")
def editar_factura(id: int, datos: FacturaCrear, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    factura.fecha = datos.fecha
    factura.cliente_id = datos.cliente_id
    session.commit()
    session.refresh(factura)
    return {"mensaje": "Factura actualizada", "factura": factura}


@rutas_facturas.delete("/facturas/{id}")
def eliminar_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    session.delete(factura)
    session.commit()
    return {"mensaje": "Factura eliminada"}
