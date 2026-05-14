from pydantic import BaseModel

class Cliente(BaseModel):
    id: int | None = None
    nombre: str
    edad: int
    descripcion: str | None = None
