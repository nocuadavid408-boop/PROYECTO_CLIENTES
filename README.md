# API Gestion de Facturas — FastAPI

API REST construida con FastAPI y SQLModel que gestiona clientes, facturas y transacciones. Permite realizar operaciones CRUD completas sobre cada recurso, con persistencia en base de datos SQLite y relaciones entre tablas.

---

## Tecnologias

| Herramienta  | Descripcion                          |
|--------------|--------------------------------------|
| Python 3.12+ | Lenguaje base                        |
| FastAPI      | Framework web para la API            |
| SQLModel     | ORM para la base de datos            |
| SQLite       | Base de datos local                  |
| Uvicorn      | Servidor ASGI                        |
| uv           | Gestor de entorno virtual            |

---

## Estructura del proyecto

```
p.y.t.h.o.n/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de la API
│   ├── database.py              # Configuracion de la base de datos
│   ├── models/
│   │   ├── cliente.py           # Modelo Cliente
│   │   ├── facturas.py          # Modelo Factura
│   │   └── transacciones.py     # Modelo Transaccion
│   └── routers/
│       ├── clientes.py          # Endpoints CRUD de clientes
│       ├── facturas.py          # Endpoints CRUD de facturas
│       └── transacciones.py     # Endpoints CRUD de transacciones
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Instalacion y ejecucion

### 1. Clonar el repositorio

```bash
git clone https://github.com/nocuadavid408-boop/PROYECTO_CLIENTES.git
cd PROYECTO_CLIENTES
```

### 2. Crear el entorno virtual con uv

```bash
python -m venv .venv    
```

### 3. Activar el entorno virtual

Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```bash
uv pip install -r requirements.txt
```

### 5. Ejecutar la API

```bash
uvicorn app.main:aplicacion --reload
```

La API queda disponible en: http://127.0.0.1:8000

Documentacion interactiva (Swagger UI): http://127.0.0.1:8000/docs

---

## Endpoints disponibles

### Clientes

| Metodo | Ruta                    | Descripcion                  |
|--------|-------------------------|------------------------------|
| GET    | /clientes               | Listar todos los clientes    |
| GET    | /clientes/{cliente_id}  | Obtener un cliente por ID    |
| POST   | /cliente/{cliente_id}   | Crear un cliente             |
| PATCH  | /cliente/{cliente_id}   | Editar un cliente            |
| DELETE | /cliente/{cliente_id}   | Eliminar un cliente          |

Cuerpo para POST / PATCH:
```json
{
  "nombre": "Juan Perez",
  "edad": 30,
  "descripcion": "Cliente frecuente"
}
```

### Facturas

| Metodo | Ruta                      | Descripcion                           |
|--------|---------------------------|---------------------------------------|
| GET    | /facturas                 | Listar todas las facturas con total   |
| GET    | /facturas/{factura_id}    | Obtener una factura por ID            |
| POST   | /facturas/{cliente_id}    | Crear una factura para un cliente     |
| PATCH  | /facturas/{factura_id}    | Editar una factura                    |
| DELETE | /facturas/{factura_id}    | Eliminar una factura                  |

Cuerpo para POST / PATCH:
```json
{
  "fecha": "2026-07-01T10:00:00"
}
```

El valor_total se calcula automaticamente sumando valor_unitario x cantidad de todas las transacciones de la factura.

### Transacciones

| Metodo | Ruta                              | Descripcion                              |
|--------|-----------------------------------|------------------------------------------|
| GET    | /transacciones                    | Listar todas las transacciones           |
| GET    | /transacciones/{transaccion_id}   | Obtener una transaccion por ID           |
| POST   | /transacciones/{factura_id}       | Crear una transaccion para una factura   |
| PATCH  | /transacciones/{transaccion_id}   | Editar una transaccion                   |
| DELETE | /transacciones/{transaccion_id}   | Eliminar una transaccion                 |

Cuerpo para POST / PATCH:
```json
{
  "cantidad": 3,
  "valor_unitario": 15000.0,
  "descripcion": "Producto A"
}
```

---

## Relaciones de base de datos

```
Cliente (1) ---- (N) Factura (1) ---- (N) Transaccion
```

- Un cliente puede tener muchas facturas
- Una factura puede tener muchas transacciones
- El valor_total se calcula en tiempo real sumando valor_unitario x cantidad

---

## Flujo recomendado de uso

```
1. Crear un cliente        ->  POST /cliente/{cliente_id}
2. Crear una factura       ->  POST /facturas/{cliente_id}
3. Agregar transacciones   ->  POST /transacciones/{factura_id}
4. Ver facturas con total  ->  GET /facturas
```

---

## Historial de versiones (commits)

| Version | Commit                                                                          | Descripcion                                          |
|---------|---------------------------------------------------------------------------------|------------------------------------------------------|
| v0      | init: proyecto inicial sin estructura, todo en main.py                          | Todo en un solo archivo, sin carpetas ni modelos     |
| v1      | feat: agregar modelos Pydantic y CRUD completo para clientes facturas y transacciones | Modelos con Pydantic, routers separados, listas en memoria |
| v2      | refactor: adaptar estructura al formato del instructor con enrutador unico       | Todo el router en un solo archivo enrutador.py       |
| v3      | feat: agregar .gitignore y corregir encoding de requirements.txt                | .gitignore y requirements.txt limpios                |
| v4      | feat: migrar a SQLModel con conexion_bd.py y modelos con table=True             | Base de datos SQLite, datos persistentes             |
| v5      | feat: agregar relaciones de BD con foreign_key y Relationship entre tablas      | Relaciones entre Cliente, Factura y Transaccion      |

---

## Comandos Git utiles

```bash
git log                        # Ver historial completo
git log --oneline              # Ver historial resumido
git checkout <hash_commit>     # Ir a una version especifica
git checkout main              # Volver al ultimo commit
```

---

## Autor

Joshua David Nocua Carrillo
Tecnologo en Analisis y Desarrollo de Software (ADSO)
SENA - Ficha 3407184
