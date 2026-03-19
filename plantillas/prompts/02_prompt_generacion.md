Implementa el proyecto COMPLETO según la arquitectura definida en el INPUT. Este es el paso más importante del pipeline: el código que entregues debe poder ejecutarse sin modificaciones.

## Reglas absolutas

**REGLA 1 — COMPLETITUD:** Genera TODOS los archivos listados en la arquitectura. Si la arquitectura define 12 archivos, entregas 12 archivos. Está terminantemente prohibido escribir comentarios como "el resto de la implementación es similar", "aquí iría el código de X", o "implementación omitida por brevedad". O escribes el código completo o no lo escribes.

**REGLA 2 — FORMATO DE ARCHIVO:** Cada archivo va precedido de su ruta completa en este formato exacto, sin excepciones:
```python filename: ruta/completa/del/archivo.py

Para archivos no-Python usa la extensión correcta:
```text filename: requirements.txt
```markdown filename: .env.example

**REGLA 3 — ORDEN DE ENTREGA:** Sigue este orden estricto para que cada archivo pueda importar al anterior sin errores:
1. requirements.txt
2. .env.example
3. manage.py
4. nexo/settings.py
5. Modelos de cada app (models.py) — empezando por las apps sin dependencias
6. Admin (admin.py) de cada app
7. Serializadores (serializers.py) de cada app
8. Servicios (services.py) de cada app — aquí va la lógica de negocio
9. Vistas (views.py) de cada app
10. URLs de cada app (urls.py) y URLs raíz
11. Tasks de Celery (tasks.py)
12. conftest.py y fixtures de desarrollo

**REGLA 4 — CALIDAD DEL CÓDIGO:**
- Type hints en todas las funciones y métodos públicos
- Manejo explícito de todos los errores (nunca `except: pass`)
- `select_for_update()` en operaciones de votación para evitar race conditions
- `select_related` / `prefetch_related` donde haya ForeignKeys en listados
- Validaciones en serializers, no en vistas
- Lógica de negocio en services.py, no en vistas ni modelos
- Constantes en lugar de strings mágicos (usa un archivo `constants.py` o enums)

**REGLA 5 — DEPENDENCIAS:** El requirements.txt incluye versiones fijadas (==) para todas las dependencias directas e indirectas relevantes.

## Al final de todos los archivos
Incluye una sección "Cómo ejecutar el proyecto" con los comandos exactos y en orden:
1. Crear entorno virtual e instalar dependencias
2. Configurar variables de entorno
3. Ejecutar migraciones
4. Crear superusuario
5. Levantar Redis (comando Docker si aplica)
6. Levantar worker de Celery
7. Levantar servidor Django
