# API REST con FastAPI

API REST construida con **FastAPI** que gestiona clientes, facturas y transacciones. Permite realizar operaciones CRUD completas sobre cada recurso.

---

## 🛠️ Tecnologías

| Herramienta | Descripción |
|-------------|-------------|
| Python 3.12+ | Lenguaje base |
| FastAPI | Framework web para la API |
| Pydantic | Validación de datos |
| Uvicorn | Servidor ASGI |
| uv | Gestor de entorno virtual y dependencias |

---

## Estructura del proyecto

```
app/
├── main.py               # Punto de entrada de la app
├── database.py           # Almacenamiento en memoria
├── models/
│   ├── clientes.py       # Modelo Cliente
│   ├── facturas.py       # Modelo Factura (con valor_total)
│   └── transacciones.py  # Modelo Transaccion
└── routers/
    ├── clientes.py       # Endpoints CRUD de clientes
    ├── facturas.py       # Endpoints CRUD de facturas
    └── transacciones.py  # Endpoints CRUD de transacciones
```

---

## ⚙️ Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd p.y.t.h.o.n
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

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 4. Instalar dependencias

```bash
uv pip install -r requirements.txt
```

### 5. Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en: **http://127.0.0.1:8000**

Documentación interactiva (Swagger UI): **http://127.0.0.1:8000/docs**

---

## Endpoints disponibles

### Clientes — `/clientes`

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
  "fecha": "2026-05-27T10:00:00",
  "cliente_id": 1
}
```

>  El `valor_total` se calcula automáticamente sumando `valor_unitario × cantidad` de todas las transacciones asociadas a esa factura.

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

>  El `factura_id` debe corresponder a una factura existente, de lo contrario retorna error 404.

---

## Flujo recomendado de uso

```
1. Crear un cliente        →  POST /clientes
2. Crear una factura       →  POST /facturas  (con el cliente_id)
3. Agregar transacciones   →  POST /transacciones  (con el factura_id)
4. Ver valor total         →  GET /facturas/{id}/valor_total
```

---

## Equipo

Proyecto desarrollado en el programa **Tecnólogo en Análisis y Desarrollo de Software (ADSO)** — SENA, Ficha 3407184 - Joshua Nocua.
