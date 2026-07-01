from fastapi import FastAPI

from app.routers.enrutador import router_clientes

app = FastAPI()


@app.get("/")
def root():
    return {"mensaje": "API funcionando"}



app.include_router(router_clientes)
