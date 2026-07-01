from fastapi import FastAPI

app = FastAPI()

# Base de datos en memoria
clientes = []
facturas = []
transacciones = []


@app.get("/")
def root():
    return {"mensaje": "API funcionando"}


# ─────────────────────────────────────────
#  CLIENTES
# ─────────────────────────────────────────

@app.get("/clientes")
def listar_clientes():
    return clientes


@app.get("/clientes/{id}")
def obtener_cliente(id: int):
    for cliente in clientes:
        if cliente["id"] == id:
            return cliente
    return {"error": "Cliente no encontrado"}


@app.post("/clientes")
def crear_cliente(nombre: str, edad: int, descripcion: str = None):
    cliente = {
        "id": len(clientes) + 1,
        "nombre": nombre,
        "edad": edad,
        "descripcion": descripcion
    }
    clientes.append(cliente)
    return {"mensaje": "Cliente creado", "cliente": cliente}


@app.put("/clientes/{id}")
def editar_cliente(id: int, nombre: str, edad: int, descripcion: str = None):
    for cliente in clientes:
        if cliente["id"] == id:
            cliente["nombre"] = nombre
            cliente["edad"] = edad
            cliente["descripcion"] = descripcion
            return {"mensaje": "Cliente actualizado", "cliente": cliente}
    return {"error": "Cliente no encontrado"}


@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for index, cliente in enumerate(clientes):
        if cliente["id"] == id:
            clientes.pop(index)
            return {"mensaje": "Cliente eliminado"}
    return {"error": "Cliente no encontrado"}


# ─────────────────────────────────────────
#  FACTURAS
# ─────────────────────────────────────────

@app.get("/facturas")
def listar_facturas():
    return facturas


@app.get("/facturas/{id}")
def obtener_factura(id: int):
    for factura in facturas:
        if factura["id"] == id:
            return factura
    return {"error": "Factura no encontrada"}


@app.get("/facturas/{id}/valor_total")
def obtener_valor_total(id: int):
    for factura in facturas:
        if factura["id"] == id:
            total = sum(
                t["valor_unitario"] * t["cantidad"]
                for t in transacciones
                if t["factura_id"] == id
            )
            return {"factura_id": id, "valor_total": total}
    return {"error": "Factura no encontrada"}


@app.post("/facturas")
def crear_factura(cliente_id: int):
    factura = {
        "id": len(facturas) + 1,
        "cliente_id": cliente_id
    }
    facturas.append(factura)
    return {"mensaje": "Factura creada", "factura": factura}


@app.put("/facturas/{id}")
def editar_factura(id: int, cliente_id: int):
    for factura in facturas:
        if factura["id"] == id:
            factura["cliente_id"] = cliente_id
            return {"mensaje": "Factura actualizada", "factura": factura}
    return {"error": "Factura no encontrada"}


@app.delete("/facturas/{id}")
def eliminar_factura(id: int):
    for index, factura in enumerate(facturas):
        if factura["id"] == id:
            facturas.pop(index)
            return {"mensaje": "Factura eliminada"}
    return {"error": "Factura no encontrada"}


# ─────────────────────────────────────────
#  TRANSACCIONES
# ─────────────────────────────────────────

@app.get("/transacciones")
def listar_transacciones():
    return transacciones


@app.get("/transacciones/{id}")
def obtener_transaccion(id: int):
    for transaccion in transacciones:
        if transaccion["id"] == id:
            return transaccion
    return {"error": "Transacción no encontrada"}


@app.post("/transacciones")
def crear_transaccion(valor_unitario: float, cantidad: int, factura_id: int):
    transaccion = {
        "id": len(transacciones) + 1,
        "valor_unitario": valor_unitario,
        "cantidad": cantidad,
        "factura_id": factura_id
    }
    transacciones.append(transaccion)
    return {"mensaje": "Transacción creada", "transaccion": transaccion}


@app.put("/transacciones/{id}")
def editar_transaccion(id: int, valor_unitario: float, cantidad: int, factura_id: int):
    for transaccion in transacciones:
        if transaccion["id"] == id:
            transaccion["valor_unitario"] = valor_unitario
            transaccion["cantidad"] = cantidad
            transaccion["factura_id"] = factura_id
            return {"mensaje": "Transacción actualizada", "transaccion": transaccion}
    return {"error": "Transacción no encontrada"}


@app.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    for index, transaccion in enumerate(transacciones):
        if transaccion["id"] == id:
            transacciones.pop(index)
            return {"mensaje": "Transacción eliminada"}
    return {"error": "Transacción no encontrada"}
