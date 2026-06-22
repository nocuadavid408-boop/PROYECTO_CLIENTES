from fastapi import FastAPI

from app.conexion_bd import crear_tablas
from app.routers.clientes import rutas_clientes
from app.routers.facturas import rutas_facturas
from app.routers.transacciones import rutas_transacciones

app = FastAPI()


@app.on_event("startup")
def on_startup():
    crear_tablas()


@app.get("/")
def root():
    return {"mensaje": "API funcionando"}


# ENRUTADORES
app.include_router(rutas_clientes)
app.include_router(rutas_facturas)
app.include_router(rutas_transacciones)
