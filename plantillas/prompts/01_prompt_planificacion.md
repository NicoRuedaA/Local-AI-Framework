Diseña la arquitectura técnica COMPLETA para el proyecto descrito en el INPUT. Este documento será la única referencia que usará el Constructor para generar el código, así que debe ser exhaustivo y sin ambigüedades.

## Entrega obligatoria

### 1. Stack tecnológico
Por cada tecnología: nombre, versión exacta, y justificación en una línea. Si el proyecto especifica tecnologías, úsalas. Solo propones alternativas si hay una razón técnica crítica, y la señalas explícitamente.

### 2. Estructura de carpetas COMPLETA
Árbol de archivos con TODOS los archivos que el Constructor deberá crear. Incluye `__init__.py`, `apps.py`, `admin.py`, `urls.py`, `settings.py`, `requirements.txt`, `manage.py`, `conftest.py`, `.env.example`. Sin omisiones.

**Regla de arquitectura — un modelo, una ubicación:** Cada modelo vive en el `models.py` de su app. NO incluyas un `models.py` en la raíz del proyecto Django (ej: `nexo/models.py`) con definiciones de modelos. Si debe existir ese archivo por razones de estructura, estará vacío.

### 3. Modelo de datos detallado
Para cada modelo Django:
- Nombre de la clase
- Todos los campos con su tipo Django exacto (`CharField(max_length=255)`, `ForeignKey(..., on_delete=CASCADE)`, etc.)
- Para campos `CharField` con `choices`: usa `TextChoices` y especifica el `max_length` calculado sobre el key más largo + margen. Ejemplo: si el key más largo es `'en_desarrollo'` (13 chars), el `max_length` mínimo es 20.
- Índices necesarios (`Meta.indexes` o `db_index=True` en el campo)
- Restricciones de unicidad usando `UniqueConstraint` en `Meta.constraints` — **nunca `unique_together`**
- El método `__str__` siempre
- **Nunca** un override de `save()` solo para gestionar fechas — para eso sirve `auto_now_add` / `auto_now`

**Regla obligatoria sobre el User model:** Si el proyecto define un modelo `User` custom:
- Especifica explícitamente `AUTH_USER_MODEL = 'app.User'` en la sección de settings
- Indica que todos los `ForeignKey` a User deben usar `settings.AUTH_USER_MODEL`

### 4. Diseño de la API REST
Para cada endpoint:
- Método HTTP + ruta
- Permisos requeridos (anónimo / autenticado / solo admin)
- Qué hace en una línea
- ViewSet o APIView recomendado

### 5. Flujo de datos críticos
Describe paso a paso los flujos más complejos del sistema. Formato: Paso 1 → Paso 2 → ...

Para flujos con concurrencia (ej: sistema de votos), especifica explícitamente:
- Qué operación requiere `select_for_update()`
- Que ese `select_for_update()` debe estar dentro de `transaction.atomic()`
- Qué garantía de unicidad existe a nivel de base de datos (UniqueConstraint en el modelo)

Para flujos con notificaciones asíncronas (ej: emails al cambiar estado):
- La task de Celery se dispara desde `perform_update` en la vista, NO desde el service
- La task verifica el estado actual del objeto al ejecutarse (idempotencia)
- La task tiene `max_retries` y `default_retry_delay`

### 6. Decisiones de diseño
Las 5 decisiones arquitectónicas más importantes con su justificación. Incluye explícitamente:
- Cómo manejas la concurrencia en el sistema de votos
- Dónde vive la lógica de notificaciones (tasks, no services)
- Por qué se usa `AUTH_USER_MODEL` en lugar de importar `User` directamente

### 7. Riesgos técnicos
3 riesgos concretos con su mitigación específica. Nada de "podría haber problemas de rendimiento" — di exactamente qué query, qué endpoint, qué volumen.

### 8. Configuración de settings.py
Especifica el contenido exacto de las secciones críticas de `settings.py`:
- `AUTH_USER_MODEL` si hay User custom
- `INSTALLED_APPS` con todas las apps del proyecto
- `REST_FRAMEWORK` con `DEFAULT_PAGINATION_CLASS`, `DEFAULT_AUTHENTICATION_CLASSES` y `DEFAULT_PERMISSION_CLASSES`
- Configuración de Celery + Redis
- **Ausencia explícita** de `CELERY_TASK_ALWAYS_EAGER` (indicar que va solo en conftest.py)
