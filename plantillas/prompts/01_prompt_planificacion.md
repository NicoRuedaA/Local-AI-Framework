Diseña la arquitectura técnica COMPLETA para el proyecto descrito en el INPUT. Este documento será la única referencia que usará el Constructor para generar el código, así que debe ser exhaustivo y sin ambigüedades.

## Entrega obligatoria

### 1. Stack tecnológico
Por cada tecnología: nombre, versión exacta, y justificación en una línea. Si el proyecto especifica tecnologías, úsalas. Solo propones alternativas si hay una razón técnica crítica, y la señalas explícitamente.

### 2. Estructura de carpetas COMPLETA
Árbol de archivos con TODOS los archivos que el Constructor deberá crear. Incluye `__init__.py`, `apps.py`, `admin.py`, `urls.py`, `settings.py`, `requirements.txt`, `manage.py`, `conftest.py`, `.env.example`. Sin omisiones.

### 3. Modelo de datos detallado
Para cada modelo Django:
- Nombre de la clase
- Todos los campos con su tipo Django exacto (`CharField(max_length=255)`, `ForeignKey(..., on_delete=CASCADE)`, etc.)
- Índices necesarios (`Meta.indexes`)
- Restricciones de unicidad (`Meta.unique_together` o `UniqueConstraint`)
- Métodos relevantes (`__str__`, `save` override si aplica)

### 4. Diseño de la API REST
Para cada endpoint:
- Método HTTP + ruta
- Permisos requeridos (anónimo / autenticado / solo admin)
- Qué hace en una línea
- ViewSet o APIView recomendado

### 5. Flujo de datos críticos
Describe paso a paso los flujos más complejos del sistema (concurrencia en votos, pipeline de notificaciones por email con Celery). Formato: Paso 1 → Paso 2 → ...

### 6. Decisiones de diseño
Las 5 decisiones arquitectónicas más importantes con su justificación. Incluye explícitamente cómo manejas la concurrencia en el sistema de votos.

### 7. Riesgos técnicos
3 riesgos concretos con su mitigación específica. Nada de "podría haber problemas de rendimiento" — di exactamente qué query, qué endpoint, qué volumen.

### 8. Configuración de Celery y Redis
Describe la configuración exacta necesaria en `settings.py` para Celery + Redis, y cómo se conecta con Django.
