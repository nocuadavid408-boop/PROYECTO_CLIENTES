from fastapi import FastAPI

from app.routers.clientes import router_clientes

app = FastAPI()


@app.get("/")
def root():
    return {"mensaje": "API funcionando"}


# ROUTERS
app.include_router(router_clientes)
