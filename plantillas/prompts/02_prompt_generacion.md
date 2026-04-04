Implementa el proyecto COMPLETO según la arquitectura definida en el INPUT. Este es el paso más importante del pipeline: el código que entregues debe poder ejecutarse sin modificaciones.

## Fase 0 — Pre-generación (obligatoria, antes de escribir código)

Antes de generar ningún archivo, completa este análisis en tu respuesta:

**0.1 — Inventario de archivos**
Lista todos los archivos que vas a generar, en el orden exacto en que los entregarás.

**0.2 — Mapa de dependencias críticas**
Responde estas preguntas sobre el proyecto:
- ¿El proyecto define un modelo `User` custom (hereda de `AbstractUser`)? → Si sí, `AUTH_USER_MODEL` es obligatorio en settings.
- ¿Qué modelos existen y en qué app vive cada uno? → Ningún modelo puede aparecer en `models.py` raíz.
- ¿Qué operaciones requieren concurrencia segura (votos, reservas, stock)? → Esas necesitan `select_for_update()` + `transaction.atomic()`.
- ¿Qué operaciones son asíncronas (emails, notificaciones, webhooks)? → Esas van en Celery tasks, nunca en services.py.
- ¿Qué apps tienen modelos? → Todas deben estar en `INSTALLED_APPS`.

**0.3 — Tabla de símbolos por archivo**
Para los archivos más complejos (`views.py`, `services.py`, `tasks.py`, `conftest.py`), lista los símbolos externos que usarás y de dónde los importarás:

```
views.py:
  - ModelViewSet → from rest_framework.viewsets import ModelViewSet
  - viewsets     → from rest_framework import viewsets
  - transaction  → from django.db import transaction
  - [etc.]

services.py:
  - [lista de símbolos y su origen]

tasks.py:
  - shared_task  → from celery import shared_task
  - send_mail    → from django.core.mail import send_mail
  - [etc.]
```

Esta tabla es tu contrato. Cuando generes cada archivo, copia los imports de aquí.

---

## Reglas absolutas

**REGLA 1 — COMPLETITUD:** Genera TODOS los archivos listados en la arquitectura. Si la arquitectura define 12 archivos, entregas 12 archivos. Está terminantemente prohibido escribir comentarios como "el resto de la implementación es similar", "aquí iría el código de X", o "implementación omitida por brevedad". O escribes el código completo o no lo escribes.

**REGLA 2 — FORMATO DE ARCHIVO:** Cada archivo va precedido de su ruta completa en este formato exacto, sin excepciones:
```[lenguaje] filename: ruta/completa/del/archivo.[ext]

Usa la extensión correcta según el tipo de archivo:
- Código fuente: la extensión del lenguaje del proyecto (`.py`, `.js`, `.ts`, `.go`...)
- Texto plano: `.txt`, `.env`, `.example`
- Markdown: `.md`

**REGLA 3 — ORDEN DE ENTREGA:** Sigue el orden natural de dependencias del stack definido en `convenciones.md`. La regla general es: entrega primero los archivos de los que dependen otros. Orden típico:
1. Archivo de dependencias del proyecto (`requirements.txt`, `package.json`, `go.mod`...)
2. Archivo de variables de entorno de ejemplo (`.env.example`)
3. Configuración del proyecto (`settings.py`, `config.js`, `application.yml`...)
4. Modelos / entidades de dominio — empezando por los que no tienen dependencias
5. Capa de acceso a datos / repositorios
6. Capa de servicios — aquí va la lógica de negocio
7. Capa de presentación / controladores / vistas
8. Rutas / URLs
9. Tareas asíncronas / workers
10. Tests y fixtures

Si el stack del proyecto requiere un orden diferente, el orden correcto es el que permite ejecutar cada archivo sin errores de import al cargarlo.

**REGLA 4 — CALIDAD DEL CÓDIGO:**
- Aplica todas las convenciones definidas en `convenciones.md` sin excepción
- Tipado estático en todas las funciones y métodos públicos (si el lenguaje lo permite)
- Manejo explícito de todos los errores — nunca errores silenciosos
- Validaciones en la capa correcta según la arquitectura (no en controladores ni modelos)
- Lógica de negocio en la capa de servicios, no en controladores ni modelos
- Constantes en lugar de strings y números mágicos

**REGLA 5 — IMPORTS:** Cada archivo importa todo lo que usa. Un símbolo importado en otro archivo del proyecto NO está disponible en el archivo actual. Usa la tabla del Paso 0.3 como referencia. Revisa cada archivo de forma completamente independiente antes de entregarlo.

**REGLA 6 — DEPENDENCIAS:** El archivo de dependencias del proyecto incluye versiones fijadas para todas las dependencias directas.

**REGLA 7 — UN MODELO, UN ARCHIVO:** Cada modelo Django se define en un único `models.py` dentro de su app. El `models.py` raíz del proyecto Django (ej: `nexo/models.py`) se entrega VACÍO con este contenido exacto:
```python
# Los modelos viven en sus respectivas apps. Este archivo se mantiene vacío.
```
No importes ni reexportes modelos desde el raíz. No copies definiciones de modelos entre archivos.

**REGLA 8 — AUTH_USER_MODEL OBLIGATORIO:** Si el proyecto define un modelo `User` custom:
1. `settings.py` DEBE incluir `AUTH_USER_MODEL = 'nombre_app.User'`
2. Todos los `ForeignKey` a User DEBEN usar `settings.AUTH_USER_MODEL`:
   ```python
   from django.conf import settings
   created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   ```
3. Las factories de test DEBEN referenciar el User custom:
   ```python
   from django.conf import settings
   class UserFactory(factory.django.DjangoModelFactory):
       class Meta:
           model = settings.AUTH_USER_MODEL
   ```

**REGLA 9 — CELERY SIEMPRE ASÍNCRONO:** El código de envío de emails, notificaciones o cualquier operación I/O pesada va SIEMPRE en una task de Celery (`tasks.py`), nunca en `services.py`. `services.py` puede llamar a `.delay()`, pero nunca a `send_mail` directamente.

**REGLA 10 — CELERY_TASK_ALWAYS_EAGER SOLO EN TESTS:** Esta variable NUNCA va en `settings.py`. Solo se activa en `conftest.py` como fixture:
```python
@pytest.fixture(autouse=True)
def celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = True
```

**REGLA 11 — TRANSACCIONES EN OPERACIONES CONCURRENTES:** Cualquier operación que use `select_for_update()` DEBE estar dentro de `with transaction.atomic():`. Sin la transacción, el lock no tiene efecto.

**REGLA 12 — max_length EN CAMPOS STATUS:** Para campos `CharField` con `choices`, el `max_length` debe cubrir el valor almacenado más largo (el key, no el label). Usa `TextChoices` con keys cortos y calcula el `max_length` con margen.

**REGLA 13 — SIN TASKS DUPLICADAS:** Cada función de task existe en un único archivo. Si la misma lógica de notificación es relevante para dos apps, vive en la app de notificaciones y se llama desde las demás. Nunca copies una task entre archivos.

## Al final de todos los archivos

Incluye el ritual de verificación completo del agente Constructor (Tabla de Verificación de Integridad) con todos los checks completados.

Luego añade una sección "Cómo ejecutar el proyecto" con los comandos exactos y en orden:
1. Instalar dependencias
2. Configurar variables de entorno
3. Preparar la base de datos (migraciones, seeds, scripts de inicialización)
4. Levantar servicios auxiliares necesarios (colas, caché, etc.)
5. Levantar el servidor o ejecutar el proyecto
6. Verificar que funciona (endpoint o comando de comprobación)
