from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from ..models.transacciones import (
    Transaccion,
    CrearTransaccion,
    TransaccionLeer,
    ActualizarTransaccion
)
from ..models.facturas import Factura
from ..database import Sesion_dependencia

enrutador_transacciones = APIRouter()


@enrutador_transacciones.get("/transacciones", response_model=list[Transaccion])
async def listar_transacciones(sesion: Sesion_dependencia):
    consulta = select(Transaccion)
    resultado = sesion.exec(consulta).all()
    return resultado


@enrutador_transacciones.post("/transacciones/{factura_id}", response_model=Transaccion)
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: CrearTransaccion,
    sesion: Sesion_dependencia
):
    factura_encontrada = sesion.get(Factura, factura_id)

    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )

    datos_transaccion_diccionario = datos_transaccion.model_dump()
    datos_transaccion_diccionario["factura_id"] = factura_id

    transaccion_nueva = Transaccion.model_validate(datos_transaccion_diccionario)

    sesion.add(transaccion_nueva)
    sesion.commit()
    sesion.refresh(transaccion_nueva)

    return transaccion_nueva


@enrutador_transacciones.get("/transacciones/{transaccion_id}", response_model=TransaccionLeer)
async def obtener_transaccion(
    transaccion_id: int,
    sesion: Sesion_dependencia
):
    transaccion_bd = sesion.get(Transaccion, transaccion_id)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la transacción"
        )

    return transaccion_bd


@enrutador_transacciones.patch("/transacciones/{transaccion_id}", response_model=TransaccionLeer)
async def actualizar_transaccion(
    transaccion_id: int,
    datos_transaccion: ActualizarTransaccion,
    sesion: Sesion_dependencia
):
    transaccion_bd = sesion.get(Transaccion, transaccion_id)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la transacción"
        )

    datos_actualizados = datos_transaccion.model_dump(exclude_unset=True)

    transaccion_bd.sqlmodel_update(datos_actualizados)

    sesion.add(transaccion_bd)
    sesion.commit()
    sesion.refresh(transaccion_bd)

    return transaccion_bd


@enrutador_transacciones.delete("/transacciones/{transaccion_id}", response_model=TransaccionLeer)
async def eliminar_transaccion(
    transaccion_id: int,
    sesion: Sesion_dependencia
):
    transaccion_bd = sesion.get(Transaccion, transaccion_id)

    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la transacción"
        )

    sesion.delete(transaccion_bd)
    sesion.commit()

    return transaccion_bd