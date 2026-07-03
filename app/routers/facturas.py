from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from ..database import Sesion_dependencia
from ..models.facturas import (
    Factura,
    CrearFactura,
    FacturaLeer,
    FacturaLeerCompuesta,
    ActualizarFactura
)
from ..models.cliente import Cliente

enrutador_facturas = APIRouter()


@enrutador_facturas.get("/facturas", response_model=list[FacturaLeerCompuesta])
async def listar_facturas(sesion: Sesion_dependencia):
    consulta = select(Factura)
    lista_facturas = sesion.exec(consulta).all()
    return lista_facturas


@enrutador_facturas.get("/facturas/{factura_id}", response_model=FacturaLeerCompuesta)
async def obtener_factura_por_id(factura_id: int, sesion: Sesion_dependencia):
    factura_bd = sesion.get(Factura, factura_id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la factura"
        )

    return factura_bd


@enrutador_facturas.post("/facturas/{cliente_id}", response_model=FacturaLeer)
async def crear_factura(
    cliente_id: int,
    datos_factura: CrearFactura,
    sesion: Sesion_dependencia
):
    cliente_encontrado = sesion.get(Cliente, cliente_id)

    if not cliente_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    datos_factura_diccionario = datos_factura.model_dump()
    datos_factura_diccionario["cliente_id"] = cliente_id

    factura_nueva = Factura.model_validate(datos_factura_diccionario)

    sesion.add(factura_nueva)
    sesion.commit()
    sesion.refresh(factura_nueva)

    return factura_nueva


@enrutador_facturas.patch("/facturas/{factura_id}", response_model=FacturaLeer)
async def actualizar_factura(
    factura_id: int,
    datos_factura: ActualizarFactura,
    sesion: Sesion_dependencia
):
    factura_bd = sesion.get(Factura, factura_id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la factura"
        )

    datos_actualizados = datos_factura.model_dump(exclude_unset=True)

    factura_bd.sqlmodel_update(datos_actualizados)

    sesion.add(factura_bd)
    sesion.commit()
    sesion.refresh(factura_bd)

    return factura_bd


@enrutador_facturas.delete("/facturas/{factura_id}", response_model=FacturaLeer)
async def eliminar_factura(factura_id: int, sesion: Sesion_dependencia):
    factura_bd = sesion.get(Factura, factura_id)

    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No existe la factura"
        )

    sesion.delete(factura_bd)
    sesion.commit()

    return factura_bd