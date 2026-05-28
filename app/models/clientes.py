from pydantic import BaseModel
from typing import Optional


class ClienteCrear(BaseModel):
    nombre: str
    edad: int
    descripcion: Optional[str] = None


class Cliente(ClienteCrear):
    id: int