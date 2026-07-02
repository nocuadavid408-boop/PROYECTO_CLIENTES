# API REST con FastAPI — Proyecto Clientes

API REST construida con **FastAPI** y **SQLModel** que gestiona clientes, facturas y transacciones. Permite realizar operaciones CRUD completas sobre cada recurso, con persistencia en base de datos SQLite y relaciones entre tablas.

---

##  Tecnologías

| Herramienta | Descripción |
|-------------|-------------|
| Python 3.12+ | Lenguaje base |
| FastAPI | Framework web para la API |
| SQLModel | ORM para la base de datos |
| SQLite | Base de datos local |
| Uvicorn | Servidor ASGI |
| uv | Gestor de entorno virtual |

---

##  Estructura del proyecto

```
p.y.t.h.o.n/
├── app/
│   ├── __init__.py
│   ├── main.py               # Punto de entrada de la API
│   ├── conexion_bd.py        # Configuración de la base de datos
│   ├── models/
│   │   ├── __init__.py
│   │   ├── clientes.py       # Modelo Cliente (table=True)
│   │   └── facturas.py       # Modelos Factura y Transaccion (table=True)
│   └── routers/
│       ├── __init__.py
│       ├── clientes.py       # Endpoints CRUD de clientes
│       ├── facturas.py       # Endpoints CRUD de facturas
│       └── transacciones.py  # Endpoints CRUD de transacciones
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/nocuadavid408-boop/PROYECTO_CLIENTES.git
cd PROYECTO_CLIENTES
```

### 2. Crear el entorno virtual con `uv`

```bash
uv venv
```

### 3. Activar el entorno virtual

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

### 4. Instalar dependencias

```bash
uv pip install -r requirements.txt
```

### 5. Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La API queda disponible en: **http://127.0.0.1:8000**

Documentación interactiva (Swagger UI): **http://127.0.0.1:8000/docs**

---

##  Endpoints disponibles

###  Clientes — `/clientes`

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/clientes` | Listar todos los clientes |
| GET | `/clientes/{id}` | Obtener un cliente por ID |
| POST | `/clientes` | Crear un cliente |
| PUT | `/clientes/{id}` | Editar un cliente |
| DELETE | `/clientes/{id}` | Eliminar un cliente |

**Cuerpo para POST / PUT:**
```json
{
  "nombre": "Juan Pérez",
  "edad": 30,
  "descripcion": "Cliente frecuente"
}
```

---

###  Facturas — `/facturas`

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/facturas` | Listar todas las facturas |
| GET | `/facturas/{id}` | Obtener una factura por ID |
| GET | `/facturas/{id}/valor_total` | Calcular el valor total de la factura |
| POST | `/facturas` | Crear una factura |
| PUT | `/facturas/{id}` | Editar una factura |
| DELETE | `/facturas/{id}` | Eliminar una factura |

**Cuerpo para POST / PUT:**
```json
{
  "cliente_id": 1
}
```

---

### Transacciones — `/transacciones`

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/transacciones` | Listar todas las transacciones |
| GET | `/transacciones/{id}` | Obtener una transacción por ID |
| POST | `/transacciones` | Crear una transacción |
| PUT | `/transacciones/{id}` | Editar una transacción |
| DELETE | `/transacciones/{id}` | Eliminar una transacción |

**Cuerpo para POST / PUT:**
```json
{
  "valor_unitario": 15000.0,
  "cantidad": 3,
  "factura_id": 1
}
```

---

## Relaciones de base de datos

```
Cliente (1) ──── (N) Factura (1) ──── (N) Transaccion
```

- Un **cliente** puede tener muchas **facturas**
- Una **factura** puede tener muchas **transacciones**
- El `valor_total` de una factura se calcula sumando `valor_unitario × cantidad` de todas sus transacciones

---

## Flujo recomendado de uso

```
1. Crear un cliente        →  POST /clientes
2. Crear una factura       →  POST /facturas        (con cliente_id)
3. Agregar transacciones   →  POST /transacciones   (con factura_id)
4. Ver valor total         →  GET /facturas/{id}/valor_total
```

---

## Historial de versiones (commits)

| Versión | Commit | Descripción |
|---------|--------|-------------|
| v0 | `init: proyecto inicial sin estructura, todo en main.py` | Todo en un solo archivo, sin carpetas ni modelos |
| v1 | `feat: agregar modelos Pydantic y CRUD completo para clientes, facturas y transacciones` | Modelos con Pydantic, routers separados, listas en memoria |
| v2 | `refactor: adaptar estructura al formato del instructor con enrutador unico` | Todo el router en un solo archivo enrutador.py |
| v3 | `feat: agregar .gitignore y corregir encoding de requirements.txt` | .gitignore y requirements.txt limpios |
| v4 | `feat: migrar a SQLModel con conexion_bd.py y modelos con table=True` | Base de datos SQLite, datos persistentes |
| v5 | `feat: agregar relaciones de BD con foreign_key y Relationship entre tablas` | Relaciones entre Cliente, Factura y Transaccion |

---


**Joshua David Nocua Carrillo**
Tecnólogo en Análisis y Desarrollo de Software (ADSO)
SENA — Ficha 3407184
