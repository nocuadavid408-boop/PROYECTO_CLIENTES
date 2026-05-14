from fastapi import FastAPI
from modelos.Cliente import Cliente 

app = FastAPI()

#APLICACION DE CLIENTES

lista_clientes:list[Cliente] = []

@app.get("/clientes")
def get_clientes():
    return {"clientes": lista_clientes}   

@app.post("/clientes",)
def crear_cliente(datos_cliente: Cliente):
    datos_cliente.id = len(lista_clientes)
    lista_clientes.append(datos_cliente)
    return {"mensaje": "cliente creado correctamente"}

@app.get("/clientes/{id}")
def get_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return {"cliente": cliente}
    return {"mensaje": "cliente no encontrado"}    

@app.put("/clientes/{id}")
def editar_cliente(id: int, dato_clientes: Cliente):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            lista_clientes[i] = dato_clientes
            return {"mensaje": "cliente actualizado"}
    return {"mensaje": "cliente no encontrado"}

@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            del lista_clientes[i]
            return {"mensaje": f"Nombre: {obj_cliente.nombre}, Edad: {obj_cliente.edad}, ID: {obj_cliente.id} eliminado correctamente"}
    return {"mensaje": "cliente no encontrado"}
