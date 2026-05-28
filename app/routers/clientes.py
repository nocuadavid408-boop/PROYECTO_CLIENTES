from fastapi import APIRouter, HTTPException

from app.models.clientes import Cliente, ClienteCrear
from app.database import lista_clientes

router_clientes = APIRouter()


# VER CLIENTES
@router_clientes.get("/clientes")
def listar_clientes():
    return lista_clientes


# VER UN CLIENTE
@router_clientes.get("/clientes/{id}")
def obtener_cliente(id: int):

    for cliente in lista_clientes:

        if cliente.id == id:
            return cliente

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


# CREAR CLIENTE
@router_clientes.post("/clientes")
def crear_cliente(cliente: Cliente):

    lista_clientes.append(cliente)

    return {
        "mensaje": "Cliente creado correctamente",
        "cliente": cliente
    }


# EDITAR CLIENTE
@router_clientes.put("/clientes/{id}")
def editar_cliente(id: int, datos_actualizados: ClienteCrear):

    for cliente in lista_clientes:

        if cliente.id == id:

            cliente.nombre = datos_actualizados.nombre
            cliente.edad = datos_actualizados.edad
            cliente.descripcion = datos_actualizados.descripcion

            return {
                "mensaje": "Cliente actualizado",
                "cliente": cliente
            }

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )


# ELIMINAR CLIENTE
@router_clientes.delete("/clientes/{id}")
def eliminar_cliente(id: int):

    for index, cliente in enumerate(lista_clientes):

        if cliente.id == id:

            lista_clientes.pop(index)

            return {
                "mensaje": "Cliente eliminado"
            }

    raise HTTPException(
        status_code=404,
        detail="Cliente no encontrado"
    )