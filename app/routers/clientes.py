# rutas o endpoints
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

from app.models.clientes import Cliente, ClienteCrear
from app.conexion_bd import get_session

rutas_clientes = APIRouter()


@rutas_clientes.get("/clientes")
def listar_clientes(session: Session = Depends(get_session)):
    return session.exec(select(Cliente)).all()


@rutas_clientes.get("/clientes/{id}")
def obtener_cliente(id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@rutas_clientes.post("/clientes")
def crear_cliente(datos: ClienteCrear, session: Session = Depends(get_session)):
    cliente = Cliente(**datos.model_dump())
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return {"mensaje": "Cliente creado correctamente", "cliente": cliente}


@rutas_clientes.put("/clientes/{id}")
def editar_cliente(id: int, datos: ClienteCrear, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    cliente.nombre = datos.nombre
    cliente.edad = datos.edad
    cliente.descripcion = datos.descripcion
    session.commit()
    session.refresh(cliente)
    return {"mensaje": "Cliente actualizado", "cliente": cliente}


@rutas_clientes.delete("/clientes/{id}")
def eliminar_cliente(id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    session.delete(cliente)
    session.commit()
    return {"mensaje": "Cliente eliminado"}
