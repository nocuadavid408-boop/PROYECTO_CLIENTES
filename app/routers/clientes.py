from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from ..database import Sesion_dependencia
from ..models.cliente import Cliente, ClienteCrear, ClienteActualizar

enrutador_clientes = APIRouter()


@enrutador_clientes.get("/clientes", response_model=list[Cliente])
async def listar_clientes(sesion: Sesion_dependencia):
    clientes = sesion.exec(select(Cliente)).all()
    return clientes


@enrutador_clientes.get(
    "/clientes/{cliente_id}",
    response_model=Cliente
)
async def listar_cliente(cliente_id: int, sesion: Sesion_dependencia):
    cliente_bd = sesion.get(Cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe el cliente"
        )

    return cliente_bd


@enrutador_clientes.post("/cliente/{cliente_id}", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear, sesion: Sesion_dependencia):
    cliente_nuevo = Cliente.model_validate(datos_cliente.model_dump())

    sesion.add(cliente_nuevo)
    sesion.commit()
    sesion.refresh(cliente_nuevo)

    return cliente_nuevo


@enrutador_clientes.patch("/cliente/{cliente_id}", response_model=Cliente)
async def actualizar_cliente(
    cliente_id: int,
    datos_cliente: ClienteActualizar,
    sesion: Sesion_dependencia
):
    cliente_bd = sesion.get(Cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe el cliente"
        )

    datos_actualizados = datos_cliente.model_dump(exclude_unset=True)

    cliente_bd.sqlmodel_update(datos_actualizados)

    sesion.add(cliente_bd)
    sesion.commit()
    sesion.refresh(cliente_bd)

    return cliente_bd


@enrutador_clientes.delete("/cliente/{cliente_id}", response_model=Cliente)
async def eliminar_cliente(cliente_id: int, sesion: Sesion_dependencia):
    cliente_bd = sesion.get(Cliente, cliente_id)

    if not cliente_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe el cliente"
        )

    sesion.delete(cliente_bd)
    sesion.commit()

    return cliente_bd