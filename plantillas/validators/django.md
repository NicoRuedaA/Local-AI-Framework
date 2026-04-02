# Reglas de validación — Django + Django REST Framework

Complementa las reglas de Python con patrones de error específicos de Django y DRF que el modelo generador comete con frecuencia.

## Errores críticos a detectar y corregir

### 1. Lógica de negocio en vistas o modelos
**Detectar:** métodos de vista (`create`, `update`, `list`) que contienen lógica de negocio directamente en lugar de delegar a un `services.py`.
**Corrección:** extrae la lógica a una función en `services.py` y llámala desde la vista.

### 2. `select_for_update()` fuera de transacción atómica
**Detectar:** uso de `.select_for_update()` sin estar dentro de `with transaction.atomic():`.
**Corrección:**
```python
from django.db import transaction

with transaction.atomic():
    obj = Model.objects.select_for_update().get(id=pk)
```

### 3. Ausencia de `permission_classes` en vistas
**Detectar:** cualquier `ViewSet` o `APIView` sin `permission_classes` definido explícitamente.
**Corrección:** añade siempre `permission_classes` aunque sea para indicar acceso público.
```python
from rest_framework.permissions import IsAuthenticated, AllowAny

class MiViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
```

### 4. Serializer con `fields = '__all__'` en endpoints de escritura
**Detectar:** serializers usados en endpoints POST/PUT/PATCH que usan `fields = '__all__'`.
**Corrección:** enumera los campos explícitamente y marca los no modificables como `read_only`.
```python
class FeatureRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureRequest
        fields = ['id', 'title', 'description', 'status']
        read_only_fields = ['id', 'status', 'created_at']
```

### 5. `CELERY_TASK_ALWAYS_EAGER = True` fuera de configuración de tests
**Detectar:** `CELERY_TASK_ALWAYS_EAGER = True` en `settings.py` principal.
**Corrección:** elimínalo de `settings.py`. Debe estar solo en `settings_test.py` o en el `conftest.py` con `@override_settings`.

### 6. Modelo custom `User` no registrado en `AUTH_USER_MODEL`
**Detectar:** existe `class User(AbstractUser)` en alguna app pero `settings.py` no tiene `AUTH_USER_MODEL`.
**Corrección:**
```python
# settings.py
AUTH_USER_MODEL = 'accounts.User'
```

### 7. Ausencia de paginación en ViewSets de listado
**Detectar:** `ModelViewSet` sin `pagination_class` y sin paginación global en `REST_FRAMEWORK`.
**Corrección:** añade paginación global en settings o por ViewSet.
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}
```

### 8. Símbolo usado en un archivo pero importado solo en otro
**Este es el error más común y más difícil de detectar.** El modelo "recuerda" que importó un símbolo en otro archivo del mismo proyecto y no lo vuelve a importar donde hace falta.

**Regla de oro: cada archivo es una isla. Un símbolo importado en `tasks.py` NO está disponible en `services.py`. Revisa CADA archivo de forma completamente independiente.**

**Caso más frecuente — `send_mail` en `services.py`:**
```python
# MAL — send_mail usada sin importar (aunque sí esté importada en tasks.py)
def notify_users(feature_request_id: int) -> None:
    ...
    send_mail(subject, message, from_email, [user.email])  # ❌ NameError en runtime

# BIEN — import explícito en el mismo archivo
from django.core.mail import send_mail

def notify_users(feature_request_id: int) -> None:
    ...
    send_mail(subject, message, from_email, [user.email])  # ✅
```

**Cómo detectarlo:** Para cada símbolo usado en el código (funciones, clases, decoradores), busca su `import` o `from ... import` dentro del MISMO archivo. Si no existe en ese archivo, falta el import. No mires otros archivos.

### 9. `conftest.py` en raíz del proyecto con imports relativos o sin imports obligatorios
**El `conftest.py` en la raíz del proyecto (no dentro de una app) es el archivo con más errores sistemáticos.** Tiene tres problemas frecuentes que deben corregirse juntos:

**Problema A — imports relativos:**
```python
# MAL — la raíz no es un paquete Python
from .models import FeatureRequest   # ❌ ImportError

# BIEN — import absoluto
from nexo.features.models import FeatureRequest  # ✅
```

**Problema B — `pytest`, `APIClient` y `factory` usados sin importar:**
```python
# MAL — se usan pero no se importan
@pytest.fixture           # ❌ NameError: pytest no definido
def admin_user():
    client = APIClient()  # ❌ NameError: APIClient no definida

# BIEN
import pytest
import factory
from rest_framework.test import APIClient
```

**Problema C — atributos de factory dentro del bloque `Meta`:**
```python
# MAL — los campos van FUERA de Meta, no dentro
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        username = factory.Sequence(lambda n: f'user{n}')  # ❌ dentro de Meta

# BIEN — Meta solo contiene model y abstract
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')  # ✅ fuera de Meta
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
```

**Cuando corrijas `conftest.py`, verifica los tres problemas siempre. Aparecen juntos.**

## Formato de entrega

Entrega únicamente los archivos que contienen errores, completos y corregidos:
```python filename: ruta/completa/del/archivo.py

Al final del output añade una tabla de confirmación:
| Archivo | Error corregido |
|---------|----------------|
| ruta/archivo.py | descripción del fix |
