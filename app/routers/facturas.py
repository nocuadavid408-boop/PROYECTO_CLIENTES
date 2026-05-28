from fastapi import APIRouter

from app.models.facturas import Factura
from app.database import lista_facturas

router_facturas = APIRouter()


# VER FACTURAS
@router_facturas.get("/facturas")
def listar_facturas():
    return lista_facturas


# CREAR FACTURA
@router_facturas.post("/facturas")
def crear_factura(factura: Factura):

    lista_facturas.append(factura)

    return {
        "mensaje": "Factura creada",
        "factura": factura
    }