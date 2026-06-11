from fastapi import APIRouter, HTTPException

from app.models.clientes import Cliente, ClienteCrear
from app.models.facturas import Factura, FacturaCrear, Transaccion, TransaccionCrear
from app.database import lista_clientes, lista_facturas, lista_transacciones

router_clientes = APIRouter()



#  CLIENTES


@router_clientes.get("/clientes")
def listar_clientes():
    return lista_clientes


@router_clientes.get("/clientes/{id}")
def obtener_cliente(id: int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@router_clientes.post("/clientes")
def crear_cliente(datos: ClienteCrear):
    nueva_id = len(lista_clientes) + 1
    cliente = Cliente(id=nueva_id, **datos.model_dump())
    lista_clientes.append(cliente)
    return {"mensaje": "Cliente creado correctamente", "cliente": cliente}


@router_clientes.put("/clientes/{id}")
def editar_cliente(id: int, datos: ClienteCrear):
    for cliente in lista_clientes:
        if cliente.id == id:
            cliente.nombre = datos.nombre
            cliente.edad = datos.edad
            cliente.descripcion = datos.descripcion
            return {"mensaje": "Cliente actualizado", "cliente": cliente}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")


@router_clientes.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    for index, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes.pop(index)
            return {"mensaje": "Cliente eliminado"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")



#  FACTURAS


@router_clientes.get("/facturas")
def listar_facturas():
    return lista_facturas


@router_clientes.get("/facturas/{id}")
def obtener_factura(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            return factura
    raise HTTPException(status_code=404, detail="Factura no encontrada")


@router_clientes.get("/facturas/{id}/valor_total")
def obtener_valor_total(id: int):
    for factura in lista_facturas:
        if factura.id == id:
            total = factura.valor_total(lista_transacciones)
            return {"factura_id": id, "valor_total": total}
    raise HTTPException(status_code=404, detail="Factura no encontrada")


@router_clientes.post("/facturas")
def crear_factura(datos: FacturaCrear):
    nueva_id = len(lista_facturas) + 1
    factura = Factura(id=nueva_id, **datos.model_dump())
    lista_facturas.append(factura)
    return {"mensaje": "Factura creada", "factura": factura}


@router_clientes.put("/facturas/{id}")
def editar_factura(id: int, datos: FacturaCrear):
    for factura in lista_facturas:
        if factura.id == id:
            factura.fecha = datos.fecha
            factura.cliente_id = datos.cliente_id
            return {"mensaje": "Factura actualizada", "factura": factura}
    raise HTTPException(status_code=404, detail="Factura no encontrada")


@router_clientes.delete("/facturas/{id}")
def eliminar_factura(id: int):
    for index, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas.pop(index)
            return {"mensaje": "Factura eliminada"}
    raise HTTPException(status_code=404, detail="Factura no encontrada")



#  TRANSACCIONES


@router_clientes.get("/transacciones")
def listar_transacciones():
    return lista_transacciones


@router_clientes.get("/transacciones/{id}")
def obtener_transaccion(id: int):
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion
    raise HTTPException(status_code=404, detail="Transacción no encontrada")


@router_clientes.post("/transacciones")
def crear_transaccion(datos: TransaccionCrear):
    factura_existe = any(f.id == datos.factura_id for f in lista_facturas)
    if not factura_existe:
        raise HTTPException(
            status_code=404,
            detail=f"No existe una factura con id {datos.factura_id}"
        )
    nueva_id = len(lista_transacciones) + 1
    transaccion = Transaccion(id=nueva_id, **datos.model_dump())
    lista_transacciones.append(transaccion)
    return {"mensaje": "Transacción creada", "transaccion": transaccion}


@router_clientes.put("/transacciones/{id}")
def editar_transaccion(id: int, datos: TransaccionCrear):
    factura_existe = any(f.id == datos.factura_id for f in lista_facturas)
    if not factura_existe:
        raise HTTPException(
            status_code=404,
            detail=f"No existe una factura con id {datos.factura_id}"
        )
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            transaccion.valor_unitario = datos.valor_unitario
            transaccion.cantidad = datos.cantidad
            transaccion.factura_id = datos.factura_id
            return {"mensaje": "Transacción actualizada", "transaccion": transaccion}
    raise HTTPException(status_code=404, detail="Transacción no encontrada")


@router_clientes.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    for index, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            lista_transacciones.pop(index)
            return {"mensaje": "Transacción eliminada"}
    raise HTTPException(status_code=404, detail="Transacción no encontrada")
