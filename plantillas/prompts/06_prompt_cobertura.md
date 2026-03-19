Escribe la suite de tests COMPLETA para el proyecto del INPUT usando pytest + pytest-django + factory_boy. Los tests deben poder ejecutarse con `pytest` desde la raíz del proyecto sin configuración adicional.

## Archivos a entregar (obligatorios)

```text filename: conftest.py
— Fixtures globales: usuarios (estándar y admin), feature requests, votos, comentarios, cliente de API autenticado y anónimo.

```python filename: tests/test_auth.py
— Tests de autenticación y autorización

```python filename: tests/test_feature_requests.py
— Tests de CRUD de feature requests

```python filename: tests/test_votes.py
— Tests del sistema de votación, incluyendo concurrencia

```python filename: tests/test_comments.py
— Tests del sistema de comentarios anidados

```python filename: tests/test_admin.py
— Tests del panel de administración y cambios de estado

```python filename: tests/test_tasks.py
— Tests de las tasks de Celery y envío de emails

## Requisitos por categoría

### Happy path (mínimo 2 tests por endpoint principal)
- Usuario autenticado crea feature request con datos válidos → 201
- Usuario autenticado vota una propuesta → 200, contador incrementado
- Admin cambia estado a "Lanzado" → 200, task de Celery encolada

### Autenticación y autorización (obligatorio para cada acción protegida)
- Usuario anónimo intenta crear feature request → 401
- Usuario estándar intenta cambiar estado de propuesta → 403
- Usuario intenta editar feature request de otro usuario → 403

### Concurrencia (crítico para este proyecto)
- Dos requests simultáneos de voto del mismo usuario a la misma propuesta → solo un voto registrado
- Test con `threading` o `django.test.Client` paralelo para simular race condition

### Edge cases
- Feature request con título vacío → 400 con mensaje descriptivo
- Votar una propuesta que no existe → 404
- Comentario anidado con profundidad máxima
- Búsqueda con caracteres especiales (SQL injection attempt)

### Errores controlados
- Base de datos no disponible durante votación → error manejado, no 500 genérico
- Task de Celery falla → reintento automático verificado

### Integraciones (Celery + email)
- Al cambiar estado a "Lanzado", la task se encola exactamente una vez
- La task envía email a cada usuario que votó y solo a ellos
- Si no hay votantes, no se envía ningún email
- Usa `@override_settings(CELERY_TASK_ALWAYS_EAGER=True)` y `django.core.mail.outbox`

## Estándares de calidad
- Nombre de test descriptivo: `test_usuario_anonimo_no_puede_crear_feature_request`
- Usa `pytest.mark.parametrize` para variantes del mismo test
- Cada test es independiente: no depende del estado de otro test
- Usa `factory_boy` para crear objetos, nunca `Model.objects.create()` directamente en tests
- Al final, incluye la lista completa de escenarios cubiertos y el comando exacto para ver cobertura: `pytest --cov=. --cov-report=html`
