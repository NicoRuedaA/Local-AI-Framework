<<<<<<< HEAD
# Convenciones Técnicas — Django 5.x + DRF

Estas convenciones son obligatorias para TODO el código generado. No son sugerencias.
=======
# Convenciones Técnicas — Proyecto Nexo (Django 5.x + DRF)

Estas convenciones son obligatorias para TODO el código generado en este proyecto. No son sugerencias.
>>>>>>> 70c08ad59bb8e415f733ff0849255c00314c8441

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
- Funciones pequeñas con un único nivel de abstracción y una sola responsabilidad (SRP).
- Idioma del código: inglés (nombres de variables, funciones, clases).
- Idioma de comentarios de lógica compleja: español.
- Nombres descriptivos. Prohibidas las abreviaturas crípticas (`usr`, `req`, `obj`).
- Constantes en `constants.py` o como enums. Prohibidos strings y números mágicos inline.
- Manejo explícito de errores. Prohibido `except: pass` y errores silenciosos.
- Máximo 1 nivel de indentación en funciones de lógica (usa early return para reducir nesting).

## Django / ORM

- Usa `select_related()` para ForeignKey/OneToOne en listados.
- Usa `prefetch_related()` para ManyToMany y relaciones inversas en listados.
- Usa `select_for_update()` SIEMPRE dentro de `with transaction.atomic():` en operaciones concurrentes.
- Usa `F()` expressions para actualizar campos numéricos atómicamente.
- Usa `get_object_or_404()` en vistas. En servicios, captura `DoesNotExist` explícitamente.
- Todos los modelos tienen `__str__` definido.
- Los campos usados en filtros frecuentes tienen `db_index=True`.
- Las restricciones de unicidad van en `Meta.constraints` con `UniqueConstraint`. Prohibido `unique_together` (deprecated desde Django 4.2).
- El `models.py` raíz del proyecto Django (ej: `nexo/models.py`) se entrega VACÍO. Los modelos viven en el `models.py` de su app, nunca en el raíz.

## Django REST Framework

- Usa `ViewSet` para recursos CRUD completos, `APIView` para endpoints custom.
- Los permisos van en `permission_classes` a nivel de ViewSet o vista, nunca inline en el método.
- Usa object-level permissions para verificar que el usuario solo accede a sus propios objetos.
- Todos los listados tienen paginación (`PageNumberPagination` en settings).
- Los serializers usan `read_only_fields` para campos no modificables por el cliente.
- Prohibido `fields = '__all__'` en serializers de escritura (POST/PUT/PATCH).

## Celery

- Las tasks son idempotentes: ejecutarlas dos veces con los mismos argumentos produce el mismo resultado.
- Todas las tasks tienen `max_retries` y `default_retry_delay` definidos.
- Las tasks no contienen lógica de negocio: llaman a servicios.
- `CELERY_TASK_ALWAYS_EAGER = True` NUNCA va en `settings.py`. Solo en `conftest.py` como fixture autouse.

## Calidad y entrega

- El código entregado debe funcionar sin modificaciones salvo configuración de entorno.
- Valida los inputs en todos los puntos de entrada: funciones públicas, endpoints, CLI.
- Prioriza legibilidad sobre brevedad cuando tengas que elegir.
- Cada archivo precedido de su ruta completa: ```python filename: ruta/completa/del/archivo.py
- El archivo completo, nunca fragmentos con "... resto del código".
- `requirements.txt` con versiones fijadas (==).
- `.env.example` con todas las variables necesarias (sin valores reales).

## Tests

- Framework: pytest + pytest-django. No unittest.TestCase salvo casos excepcionales.
- Fixtures: factory_boy. No `Model.objects.create()` directamente en tests.
- Nombres descriptivos: `test_usuario_no_puede_votar_su_propia_propuesta`.
- Cada test es independiente del estado de otros tests.
- Los tests de Celery usan `CELERY_TASK_ALWAYS_EAGER = True` vía fixture, no en settings.
- Los tests de email usan `django.core.mail.outbox`.
