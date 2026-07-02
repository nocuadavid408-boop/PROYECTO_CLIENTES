from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models.clientes import (
    Cliente,
    ClienteCrear,
    ClienteActualizar,
    ClientePublico,
)

router_clientes = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

# LISTAR CLIENTES
@router_clientes.get(
    "/",
    response_model=list[ClientePublico]
)
async def listar_clientes(
    session: Session = Depends(get_session)
):
    return session.exec(
        select(Cliente)
    ).all()


# OBTENER CLIENTE
@router_clientes.get(
    "/{id}",
    response_model=ClientePublico,
    responses={
        404: {
            "description":
            "Cliente no encontrado"
        }
    }
)
async def obtener_cliente(
    id: int,
    session: Session = Depends(get_session)
):
    cliente = session.get(
        Cliente,
        id
    )

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    return cliente


# CREAR CLIENTE
@router_clientes.post(
    "/",
    response_model=ClientePublico,
    status_code=status.HTTP_201_CREATED
)
async def crear_cliente(
    datos: ClienteCrear,
    session: Session = Depends(get_session)
):

    cliente = Cliente.model_validate(
        datos
    )

    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    return cliente


# ACTUALIZAR CLIENTE
@router_clientes.put(
    "/{id}",
    response_model=ClientePublico,
    responses={
        404: {
            "description":
            "Cliente no encontrado"
        }
    }
)
async def actualizar_cliente(
    id: int,
    datos: ClienteActualizar,
    session: Session = Depends(get_session)
):

    cliente = session.get(
        Cliente,
        id
    )

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    if datos.nombre is not None:
        cliente.nombre = datos.nombre

    if datos.edad is not None:
        cliente.edad = datos.edad

    if datos.descripcion is not None:
        cliente.descripcion = datos.descripcion

    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    return cliente


# ELIMINAR CLIENTE
@router_clientes.delete(
    "/{id}",
    responses={
        404: {
            "description":
            "Cliente no encontrado"
        }
    }
)
async def eliminar_cliente(
    id: int,
    session: Session = Depends(get_session)
):

    cliente = session.get(
        Cliente,
        id
    )

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    session.delete(cliente)
    session.commit()

    return {
        "mensaje":
        "Cliente eliminado correctamente"
    }