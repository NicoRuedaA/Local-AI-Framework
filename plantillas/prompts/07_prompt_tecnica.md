Genera la documentación técnica COMPLETA del proyecto del INPUT. La documentación debe ser tan buena que un desarrollador externo pueda levantar el proyecto y contribuir sin preguntarle nada a nadie.

## Archivos a entregar

### README.md principal
```markdown filename: README.md

Estructura obligatoria:
1. **Descripción** — Qué es Nexo, qué problema resuelve, para quién es. Máximo 3 frases. Sin marketing.
2. **Arquitectura** — Diagrama en texto (ASCII) del sistema: Django ↔ PostgreSQL ↔ Redis ↔ Celery Worker
3. **Requisitos previos** — Python 3.11+, PostgreSQL 15+, Redis 7+. Versiones exactas.
4. **Instalación** — Comandos copy-paste, en orden, que funcionan en una terminal limpia:
   - Clonar repo
   - Crear virtualenv
   - Instalar dependencias
   - Configurar .env
   - Migraciones
   - Crear superusuario
   - Levantar Redis
   - Levantar Celery worker
   - Levantar servidor
5. **Variables de entorno** — Tabla completa: Variable | Descripción | Ejemplo | Obligatoria
6. **Cómo ejecutar los tests** — Comando exacto + cómo ver el reporte de cobertura
7. **Estructura del proyecto** — Árbol completo con descripción de cada carpeta y archivo relevante
8. **Documentación de la API** — Para cada endpoint:
   - Método + Ruta
   - Descripción en una línea
   - Autenticación requerida
   - Request body (JSON de ejemplo)
   - Response exitosa (JSON de ejemplo con status code)
   - Errores posibles (status code + mensaje)
9. **Guía de contribución** — Cómo crear una rama, convenciones de commits, cómo ejecutar tests antes de un PR

### Docstrings inline
```python filename: nexo/features/services.py (con docstrings)

Añade docstrings estilo Google a todas las funciones públicas de services.py:
- Una línea de resumen
- Args: nombre (tipo): descripción
- Returns: tipo: descripción
- Raises: ExceptionType: cuándo se lanza
- Example: ejemplo de uso en una línea

### Guía de despliegue
```markdown filename: docs/DEPLOYMENT.md

- Configuración de PostgreSQL en producción
- Variables de entorno de producción (qué cambiar respecto a desarrollo)
- Configuración de Celery con Supervisor o systemd
- Checklist pre-despliegue (migraciones, collectstatic, tests)
