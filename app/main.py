from fastapi import FastAPI

from app.routers.clientes import router_clientes
from app.routers.facturas import router_facturas
from app.routers.transacciones import router_transacciones

app = FastAPI()


@app.get("/")
def root():
    return {"mensaje": "API funcionando"}


# ROUTERS

app.include_router(router_clientes)
app.include_router(router_facturas)
app.include_router(router_transacciones)