from fastapi import APIRouter

from app.models.transacciones import Transaccion
from app.database import lista_transacciones

router_transacciones = APIRouter()


# VER TRANSACCIONES
@router_transacciones.get("/transacciones")
def listar_transacciones():
    return lista_transacciones


# CREAR TRANSACCION
@router_transacciones.post("/transacciones")
def crear_transaccion(transaccion: Transaccion):

    lista_transacciones.append(transaccion)

    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion
    }