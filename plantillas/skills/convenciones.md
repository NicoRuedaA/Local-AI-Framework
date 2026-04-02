# Convenciones Técnicas — Proyecto Nexo (Django 5.x + DRF)

Estas convenciones son obligatorias para TODO el código generado en este proyecto. No son sugerencias.

## Stack exacto
- Python 3.11+
- Django 5.x
- Django REST Framework 3.15+
- Celery 5.x + Redis como broker
- PostgreSQL 15+ (producción) / SQLite (desarrollo local aceptable)
- pytest + pytest-django + factory_boy para tests

## Arquitectura de capas (obligatoria)

```
Vista (views.py)        → Orquesta. Valida autenticación. Llama al servicio. Devuelve respuesta.
Serializador            → Valida inputs. Transforma datos. NUNCA contiene lógica de negocio.
Servicio (services.py)  → Contiene TODA la lógica de negocio. Es la capa testeable.
Modelo (models.py)      → Define estructura y relaciones. Métodos solo para lógica directamente ligada al modelo (__str__, propiedades).
Task (tasks.py)         → Solo llama a servicios. No contiene lógica de negocio propia.
```

**Prohibido:** lógica de negocio en vistas, en modelos o en serializers.

## Código Python

- Type hints en TODAS las funciones y métodos públicos, sin excepción.
- Idioma del código: inglés (nombres de variables, funciones, clases, comentarios de código).
- Idioma de comentarios de lógica compleja: español.
- Nombres descriptivos. Prohibidas las abreviaturas crípticas (`usr`, `req`, `obj`).
- Constantes en `constants.py` o como enums. Prohibidos strings y números mágicos inline.
- Manejo explícito de errores. Prohibido `except: pass` y errores silenciosos.
- Máximo 1 nivel de indentación en funciones de lógica (usa early return para reducir nesting).

## Django / ORM

- Usa `select_related()` para ForeignKey/OneToOne en listados.
- Usa `prefetch_related()` para ManyToMany y relaciones inversas en listados.
- Usa `select_for_update()` en operaciones que requieran atomicidad (sistema de votos).
- Usa `F()` expressions para actualizar campos numéricos atómicamente.
- Usa `get_object_or_404()` en vistas. En servicios, captura `DoesNotExist` explícitamente.
- Todos los modelos tienen `__str__` definido.
- Los campos usados en filtros frecuentes tienen `db_index=True`.
- Las restricciones de unicidad van en `Meta.constraints` con `UniqueConstraint`, no en `unique_together` (deprecated).

## Django REST Framework

- Usa `ViewSet` para recursos CRUD completos, `APIView` para endpoints custom.
- Los permisos van en `permission_classes` a nivel de ViewSet o vista, nunca inline en el método.
- Usa `object-level permissions` para verificar que el usuario solo accede a sus propios objetos.
- Todos los listados tienen paginación (`PageNumberPagination`).
- Los serializers usan `read_only_fields` para campos que no deben ser modificables por el cliente.

## Celery

- Las tasks son idempotentes: ejecutarlas dos veces con los mismos argumentos produce el mismo resultado.
- Todas las tasks tienen `max_retries` y `default_retry_delay` definidos.
- Las tasks no contienen lógica de negocio: llaman a servicios.
- Usa `apply_async` con `countdown` para tasks que deben ejecutarse con delay.

## Formato de entrega de código

- Cada archivo precedido de su ruta completa:
  ```python filename: ruta/completa/del/archivo.py
- El archivo completo, nunca fragmentos con "... resto del código".
- `requirements.txt` con versiones fijadas (==).
- `.env.example` con todas las variables necesarias (sin valores reales).

## Tests

- Framework: pytest + pytest-django. No unittest.TestCase salvo casos excepcionales.
- Fixtures: factory_boy. No `Model.objects.create()` directamente en tests.
- Nombres descriptivos: `test_usuario_no_puede_votar_su_propia_propuesta`.
- Cada test es independiente del estado de otros tests.
- Los tests de Celery usan `CELERY_TASK_ALWAYS_EAGER=True`.
- Los tests de email usan `django.core.mail.outbox`.
