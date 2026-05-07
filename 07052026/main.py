from fastapi import FastAPI
from pydantic import BaseModel

    
app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "hola mundo"} 

#APLICACION DE CLIENTES

lista_clientes = []
class Cliente(BaseModel):
    id:int
    nombre:str
    edad:int
    descripcion:str | None = None



@app.get("/clientes")
def get_clientes():
    return {"clientes": lista_clientes}   

@app.post("/clientes",)
def crear_cliente(datos_cliente: Cliente):
    lista_clientes.append(datos_cliente)
    return {"mensaje": "cliente creado"}

@app.get("/clientes/{id}")
def get_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return {"cliente": cliente}
    return {"mensaje": "cliente no encontrado"}    