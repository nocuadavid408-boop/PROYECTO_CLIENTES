

Versión inicial del proyecto: todo el código en un único archivo `main.py`, sin separación en carpetas. Incluye CRUD completo para clientes, facturas y transacciones, con almacenamiento en memoria.



```bash
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
uvicorn main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs
