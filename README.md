# API REST con FastAPI — SQLModel + Relaciones de BD

API REST construida con FastAPI y SQLModel. Gestiona clientes, facturas y transacciones con relaciones reales de base de datos (Foreign Keys + Relationship).

## Relación de tablas

```
Cliente (1) ──< Factura (1) ──< Transaccion
```

- Un cliente puede tener muchas facturas (`Factura.cliente_id` → FK a `cliente.id`)
- Una factura puede tener muchas transacciones (`Transaccion.factura_id` → FK a `factura.id`)
- Usa `Relationship()` de SQLModel para navegar entre objetos relacionados directamente (ej. `factura.transacciones`, `factura.cliente`)

## Estructura

```
app/
├── main.py
├── conexion_bd.py        # Motor SQLite + Session
├── models/
│   ├── clientes.py        # Cliente con Relationship a Factura
│   └── facturas.py        # Factura y Transaccion con FKs y Relationship
└── routers/
    ├── clientes.py
    ├── facturas.py
    └── transacciones.py
```

## Ejecución

```bash
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
uvicorn app.main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

Los datos persisten en `base_datos.db` (SQLite) gracias a `table=True` en los modelos.

3407184 - Joshua Nocua 
