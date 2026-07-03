from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

# Ruta de la base de datos SQLite
URL_BASE_DATOS = "sqlite:///base_datos.db"

# Crear el motor de conexión
motor_base_datos = create_engine(
    URL_BASE_DATOS,
    echo=False
)

# Función para obtener una sesión de la base de datos
def obtener_sesion():
    with Session(motor_base_datos) as sesion:
        yield sesion

# Dependencia para FastAPI
Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]

# Función que crea las tablas al iniciar la aplicación
@asynccontextmanager
async def crear_tablas(app):
    SQLModel.metadata.create_all(motor_base_datos)
    yield