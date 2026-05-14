from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# --- MODELOS ---
class Cliente(BaseModel):
    nombre: str
    edad: int
    descripcion: str | None = None

class Factura(BaseModel):
    cliente_id: int
    monto: float
    concepto: str

class Transaccion(BaseModel):
    factura_id: int
    metodo_pago: str  # Ejemplo: Efectivo, Tarjeta
    estado: str = "Completada"

# --- BASES DE DATOS TEMPORALES Y CONTADORES ---
lista_clientes = []
lista_facturas = []
lista_transacciones = []

id_cliente_inc = 1
id_factura_inc = 1
id_transaccion_inc = 1

# --- 1. INICIO ---
@app.get("/")
def inicio():
    return {"mensaje": "Sistema Integral ReCal Tech - FastAPI"}

# --- 2. APARTADO CLIENTES (GET, POST, PUT, DELETE) ---
@app.get("/clientes")
def listar_clientes():
    return {"Clientes": lista_clientes}

@app.post("/clientes")
def crear_cliente(datos: Cliente):
    global id_cliente_inc
    nuevo = datos.model_dump()
    nuevo["id"] = id_cliente_inc
    lista_clientes.append(nuevo)
    id_cliente_inc += 1
    return {"mensaje": "Cliente creado satisfactoriamente", "cliente": nuevo}

@app.put("/clientes/{id}")
def editar_cliente(id: int, datos: Cliente):
    for i, obj in enumerate(lista_clientes):
        if obj["id"] == id:
            actualizado = datos.model_dump()
            actualizado["id"] = id
            lista_clientes[i] = actualizado
            return {"mensaje": "Cliente actualizado", "Cliente": actualizado}
    return {"error": "No encontrado"}

@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for i, obj in enumerate(lista_clientes):
        if obj["id"] == id:
            eliminado = lista_clientes.pop(i)
            return {"mensaje": "Cliente eliminado", "datos_eliminados": eliminado}
    return {"error": "No encontrado"}

# --- 3. APARTADO FACTURAS (POST y GET) ---
@app.get("/facturas")
def listar_facturas():
    return {"Facturas": lista_facturas}

@app.post("/facturas")
def crear_factura(datos: Factura):
    global id_factura_inc
    # Validación: ¿Existe el cliente?
    if not any(c["id"] == datos.cliente_id for c in lista_clientes):
        return {"error": "El cliente no existe"}

    nueva_f = datos.model_dump()
    nueva_f["id"] = id_factura_inc
    nueva_f["fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lista_facturas.append(nueva_f)
    id_factura_inc += 1
    return {"mensaje": "Factura generada", "factura": nueva_f}

# --- 4. APARTADO TRANSACCIONES (POST y GET) ---
@app.get("/transacciones")
def listar_transacciones():
    return {"Transacciones": lista_transacciones}

@app.post("/transacciones")
def crear_transaccion(datos: Transaccion):
    global id_transaccion_inc
    # Validación: ¿Existe la factura?
    if not any(f["id"] == datos.factura_id for f in lista_facturas):
        return {"error": "La factura no existe"}

    nueva_t = datos.model_dump()
    nueva_t["id"] = id_transaccion_inc
    nueva_t["fecha_pago"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lista_transacciones.append(nueva_t)
    id_transaccion_inc += 1
    return {"mensaje": "Transacción registrada", "detalle": nueva_t} 