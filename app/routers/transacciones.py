from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session

from app.models.transacciones import (
    Transaccion,
    TransaccionCrear,
    TransaccionActualizar,
    TransaccionPublica,
    TransaccionDetalle
)

from app.models.facturas import Factura
from app.models.clientes import Cliente

router_transacciones = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)

# LISTAR TRANSACCIONES
@router_transacciones.get(
    "/",
    response_model=list[TransaccionDetalle]
)
async def listar_transacciones(
    session: Session = Depends(get_session)
):

    transacciones = session.exec(
        select(Transaccion)
    ).all()

    resultado = []

    for t in transacciones:

        factura = session.get(
            Factura,
            t.factura_id
        )

        cliente = session.get(
            Cliente,
            factura.cliente_id
        )

        transacciones_factura = session.exec(
            select(Transaccion)
            .where(
                Transaccion.factura_id
                == factura.id
            )
        ).all()

        total_factura = sum(
            x.valor_unitario * x.cantidad
            for x in transacciones_factura
        )

        resultado.append(
            {
                "id": t.id,

                "descripcion":
                    t.descripcion,

                "valor_unitario":
                    t.valor_unitario,

                "cantidad":
                    t.cantidad,

                "subtotal":
                    t.valor_unitario *
                    t.cantidad,

                "factura": {
                    "id": factura.id,
                    "fecha": factura.fecha
                },

                "cliente": {
                    "id": cliente.id,
                    "nombre": cliente.nombre,
                    "edad": cliente.edad,
                    "descripcion":
                        cliente.descripcion
                },

                "valor_total_factura":
                    total_factura
            }
        )

    return resultado


# OBTENER TRANSACCION
@router_transacciones.get(
    "/{id}",
    response_model=TransaccionDetalle,
    responses={
        404: {
            "description":
            "Transacción no encontrada"
        }
    }
)
async def obtener_transaccion(
    id: int,
    session: Session = Depends(get_session)
):

    t = session.get(
        Transaccion,
        id
    )

    if not t:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    factura = session.get(
        Factura,
        t.factura_id
    )

    cliente = session.get(
        Cliente,
        factura.cliente_id
    )

    transacciones_factura = session.exec(
        select(Transaccion)
        .where(
            Transaccion.factura_id
            == factura.id
        )
    ).all()

    total_factura = sum(
        x.valor_unitario * x.cantidad
        for x in transacciones_factura
    )

    return {
        "id": t.id,

        "descripcion":
            t.descripcion,

        "valor_unitario":
            t.valor_unitario,

        "cantidad":
            t.cantidad,

        "subtotal":
            t.valor_unitario *
            t.cantidad,

        "factura": {
            "id": factura.id,
            "fecha": factura.fecha
        },

        "cliente": {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "edad": cliente.edad,
            "descripcion":
                cliente.descripcion
        },

        "valor_total_factura":
            total_factura
    }


# CREAR TRANSACCION
@router_transacciones.post(
    "/",
    response_model=TransaccionPublica,
    status_code=status.HTTP_201_CREATED
)
async def crear_transaccion(
    datos: TransaccionCrear,
    session: Session = Depends(get_session)
):

    factura = session.get(
        Factura,
        datos.factura_id
    )

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    transaccion = Transaccion(
        descripcion=datos.descripcion,
        valor_unitario=datos.valor_unitario,
        cantidad=datos.cantidad,
        factura_id=datos.factura_id
    )

    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)

    return {
        "id": transaccion.id,
        "descripcion":
            transaccion.descripcion,
        "valor_unitario":
            transaccion.valor_unitario,
        "cantidad":
            transaccion.cantidad,
        "factura_id":
            transaccion.factura_id,
        "subtotal":
            transaccion.subtotal
    }


# ACTUALIZAR TRANSACCION
@router_transacciones.put(
    "/{id}",
    response_model=TransaccionPublica,
    responses={
        404: {
            "description":
            "Transacción no encontrada"
        }
    }
)
async def actualizar_transaccion(
    id: int,
    datos: TransaccionActualizar,
    session: Session = Depends(get_session)
):

    transaccion = session.get(
        Transaccion,
        id
    )

    if not transaccion:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    if datos.descripcion is not None:
        transaccion.descripcion = datos.descripcion

    if datos.valor_unitario is not None:
        transaccion.valor_unitario = datos.valor_unitario

    if datos.cantidad is not None:
        transaccion.cantidad = datos.cantidad

    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)

    return {
        "id": transaccion.id,
        "descripcion":
            transaccion.descripcion,
        "valor_unitario":
            transaccion.valor_unitario,
        "cantidad":
            transaccion.cantidad,
        "factura_id":
            transaccion.factura_id,
        "subtotal":
            transaccion.subtotal
    }


# ELIMINAR TRANSACCION
@router_transacciones.delete(
    "/{id}",
    responses={
        404: {
            "description":
            "Transacción no encontrada"
        }
    }
)
async def eliminar_transaccion(
    id: int,
    session: Session = Depends(get_session)
):

    transaccion = session.get(
        Transaccion,
        id
    )

    if not transaccion:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )

    session.delete(transaccion)
    session.commit()

    return {
        "mensaje":
        "Transacción eliminada correctamente"
    } 
    