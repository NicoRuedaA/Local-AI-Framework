# Reglas de validación — FastAPI

Complementa las reglas de Python con patrones de error específicos de FastAPI.

## Errores críticos a detectar y corregir

### 1. Operaciones de base de datos sin sesión async
**Detectar:** uso de `session.query()` (estilo síncrono) en rutas `async def`.
**Corrección:** usa el estilo async de SQLAlchemy.
```python
# Mal (en ruta async)
result = session.query(User).filter(User.id == user_id).first()

# Bien
result = await session.execute(select(User).where(User.id == user_id))
user = result.scalar_one_or_none()
```

### 2. Dependencias inyectadas sin `Depends`
**Detectar:** instanciación directa de servicios o sesiones dentro de la función de ruta.
**Corrección:** usa el sistema de inyección de dependencias de FastAPI.
```python
# Mal
@app.get("/users/{id}")
async def get_user(id: int):
    db = SessionLocal()  # ❌

# Bien
@app.get("/users/{id}")
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
```

### 3. Modelos Pydantic sin validación de tipos estricta
**Detectar:** campos de modelos Pydantic sin tipo anotado.
**Corrección:** todos los campos deben tener tipo explícito.
```python
# Mal
class UserCreate(BaseModel):
    username  # ❌ sin tipo

# Bien
class UserCreate(BaseModel):
    username: str
    email: EmailStr
```

### 4. Rutas sin `response_model`
**Detectar:** endpoints que devuelven datos de usuario/base de datos sin `response_model` definido.
**Corrección:** define siempre `response_model` para controlar qué campos se exponen.
```python
@app.get("/users/{id}", response_model=UserResponse)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
```

### 5. Excepciones no manejadas como `HTTPException`
**Detectar:** `raise Exception(...)` o excepciones genéricas dentro de rutas.
**Corrección:** convierte a `HTTPException` con el status code correcto.
```python
from fastapi import HTTPException, status

raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Usuario no encontrado"
)
```

### 6. Secrets o configuración hardcodeada
**Detectar:** `SECRET_KEY = "valor_literal"` u otras configuraciones sensibles hardcodeadas.
**Corrección:** usa `pydantic-settings` con variables de entorno.
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str

    class Config:
        env_file = ".env"
```

## Formato de entrega

Entrega únicamente los archivos que contienen errores, completos y corregidos:
```python filename: ruta/completa/del/archivo.py

Al final del output añade una tabla de confirmación:
| Archivo | Error corregido |
|---------|----------------|
| ruta/archivo.py | descripción del fix |
