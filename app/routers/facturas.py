from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.facturas import (
    Factura,
    FacturaCrear,
    FacturaActualizar,
    FacturaPublica,
    FacturaDetalle
)

from app.models.clientes import (
    Cliente
)

from app.models.transacciones import (
    Transaccion
)

router_facturas = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)


# LISTAR FACTURAS
@router_facturas.get(
    "/",
    response_model=list[FacturaDetalle]
)
async def listar_facturas(
    session: Session = Depends(get_session)
):

    facturas = session.exec(
        select(Factura)
    ).all()

    resultado = []

    for factura in facturas:

        cliente = session.get(
            Cliente,
            factura.cliente_id
        )

        transacciones = session.exec(
            select(Transaccion)
            .where(
                Transaccion.factura_id
                == factura.id
            )
        ).all()

        lista_transacciones = []
        total = 0

        for t in transacciones:

            subtotal = (
                t.valor_unitario *
                t.cantidad
            )

            total += subtotal

            lista_transacciones.append(
                {
                    "id": t.id,
                    "descripcion": t.descripcion,
                    "valor_unitario": t.valor_unitario,
                    "cantidad": t.cantidad,
                    "subtotal": subtotal
                }
            )

        resultado.append(
            {
                "id": factura.id,
                "fecha": factura.fecha,
                "cliente": {
                    "id": cliente.id,
                    "nombre": cliente.nombre,
                    "edad": cliente.edad,
                    "descripcion": cliente.descripcion
                },
                "transacciones": lista_transacciones,
                "valor_total": total
            }
        )

    return resultado


# OBTENER FACTURA
@router_facturas.get(
    "/{id}",
    response_model=FacturaDetalle,
    responses={
        404: {
            "description":
            "Factura no encontrada"
        }
    }
)
async def obtener_factura(
    id: int,
    session: Session = Depends(get_session)
):

    factura = session.get(
        Factura,
        id
    )

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    cliente = session.get(
        Cliente,
        factura.cliente_id
    )

    transacciones = session.exec(
        select(Transaccion)
        .where(
            Transaccion.factura_id
            == factura.id
        )
    ).all()

    lista_transacciones = []
    total = 0

    for t in transacciones:

        subtotal = (
            t.valor_unitario *
            t.cantidad
        )

        total += subtotal

        lista_transacciones.append(
            {
                "id": t.id,
                "descripcion": t.descripcion,
                "valor_unitario": t.valor_unitario,
                "cantidad": t.cantidad,
                "subtotal": subtotal
            }
        )

    return {
        "id": factura.id,
        "fecha": factura.fecha,
        "cliente": {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "edad": cliente.edad,
            "descripcion": cliente.descripcion
        },
        "transacciones": lista_transacciones,
        "valor_total": total
    }


# CREAR FACTURA
@router_facturas.post(
    "/",
    response_model=FacturaPublica,
    status_code=status.HTTP_201_CREATED
)
async def crear_factura(
    datos: FacturaCrear,
    session: Session = Depends(get_session)
):

    cliente = session.get(
        Cliente,
        datos.cliente_id
    )

    if not cliente:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    factura = Factura(
        cliente_id=datos.cliente_id,
        fecha=datetime.now()
    )

    session.add(factura)
    session.commit()
    session.refresh(factura)

    return factura


# ACTUALIZAR FACTURA
@router_facturas.put(
    "/{id}",
    responses={
        404: {
            "description":
            "Factura no encontrada"
        }
    }
)
async def actualizar_factura(
    id: int,
    session: Session = Depends(get_session)
):

    factura = session.get(
        Factura,
        id
    )

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    return {
        "mensaje":
        "La factura no requiere actualización"
    }


# ELIMINAR FACTURA
@router_facturas.delete(
    "/{id}",
    responses={
        404: {
            "description":
            "Factura no encontrada"
        }
    }
)
async def eliminar_factura(
    id: int,
    session: Session = Depends(get_session)
):

    factura = session.get(
        Factura,
        id
    )

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    session.delete(factura)
    session.commit()

    return {
        "mensaje":
        "Factura eliminada correctamente"
    }