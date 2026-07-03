from fastapi import FastAPI
from .routers.clientes import enrutador_clientes
from .routers.facturas import enrutador_facturas
from .routers.transacciones import enrutador_transacciones
from .database import crear_tablas

aplicacion = FastAPI(
    title="API Gestión de Facturas",
    description="API REST para gestionar clientes, facturas y transacciones",
    version="1.0.0",
    lifespan=crear_tablas
)

# Enrutador de Clientes
aplicacion.include_router(enrutador_clientes, tags=["Clientes"])
# Enrutador de Facturas
aplicacion.include_router(enrutador_facturas, tags=["Facturas"])
# Enrutador de Transacciones
aplicacion.include_router(enrutador_transacciones, tags=["Transacciones"])

# Comandos de Git
# git log
# Muestra el historial de cambios.
# git log --oneline
# Muestra el historial resumido en una sola línea.
# git checkout <código_del_commit>
# Permite cambiar a un commit específico.
