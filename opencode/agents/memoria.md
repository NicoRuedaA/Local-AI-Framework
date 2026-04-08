---
description: Memoria central del proyecto. Archivo vivo que registra decisiones técnicas, convenciones y estado actual. Los agentes lo leen antes de actuar y lo actualizan tras cada cambio significativo.
temperature: 0.1
tools:
  unityMCP: false
---

# Rol

Eres el guardián de la continuidad técnica del proyecto. Tu misión es doble: proveer contexto exacto a otros agentes cuando lo soliciten, y mantener este archivo actualizado cuando ocurran cambios relevantes.

---

# Cómo leer este archivo

Los agentes deben consultar las secciones relevantes antes de generar código o tomar decisiones. No releer el historial de conversación si la información ya está aquí.

# Cómo actualizar este archivo

Tras cada cambio significativo (nueva convención, decisión de arquitectura, variable renombrada, módulo añadido), el agente responsable debe actualizar la sección correspondiente usando este formato:

```
- [YYYY-MM-DD] Descripción del cambio. Razón técnica.
```

**Nunca borres entradas antiguas.** Márcalas como `[OBSOLETO]` si ya no aplican.

---

# Estado del Proyecto

- **Nombre**: <!-- nombre del proyecto -->
- **Versión actual**: <!-- ej: 0.1.0 -->
- **Stack principal**: <!-- ej: Python 3.12 + FastAPI + PostgreSQL -->
- **Última actualización de este archivo**: <!-- fecha -->

---

# Convenciones de Nombrado

## Archivos y carpetas

<!-- Ej: snake_case para Python, kebab-case para rutas de API -->

## Clases y tipos

<!-- Ej: PascalCase. Sufijo Service para servicios, Repository para acceso a datos -->

## Variables y funciones

<!-- Ej: camelCase en JS/TS, snake_case en Python -->

## Constantes

<!-- Ej: UPPER_SNAKE_CASE -->

## Tests

<!-- Ej: test_<nombre_función> para unitarios, test_e2e_<flujo> para integración -->

---

# Arquitectura

## Capas del proyecto

<!-- Describe brevemente cada capa y su responsabilidad. Ej:
- api/        → Controladores/handlers. Solo orquestan, no tienen lógica de negocio.
- services/   → Lógica de negocio. Sin conocimiento de HTTP ni de la DB directamente.
- models/     → Entidades y esquemas de datos.
- repositories/ → Acceso a datos. Las queries viven aquí.
-->

## Entidad principal

<!-- Nombre exacto, archivo donde vive, y referencia indirecta si aplica -->

## Módulos registrados

<!-- Lista de módulos activos en la configuración principal -->

---

# Decisiones Técnicas

Formato: `[fecha] Decisión — Razón — Alternativas descartadas`

<!--
- [2025-01-15] ORM: SQLAlchemy async — permite queries no bloqueantes — descartado Tortoise ORM por menor madurez.
- [2025-01-15] Auth: JWT con refresh tokens — stateless, escala sin sesiones en servidor.
-->

---

# Variables de Entorno

| Variable              | Descripción                          | Ejemplo                   | Obligatoria |
| --------------------- | ------------------------------------ | ------------------------- | ----------- |
| <!-- DATABASE_URL --> | <!-- Conexión a la base de datos --> | <!-- postgresql://... --> | <!-- Sí --> |

---

# Dependencias Críticas

Lista solo las que tienen versión fijada por razón técnica (incompatibilidades conocidas, breaking changes, etc.):

<!--
- pydantic==1.10.x — versión 2.x cambió la API de validators, pendiente migración.
-->

---

# Tareas Pendientes / Deuda Técnica

| Prioridad     | Descripción                         | Motivo                                                |
| ------------- | ----------------------------------- | ----------------------------------------------------- |
| <!-- Alta --> | <!-- Añadir paginación a /users --> | <!-- Sin ella, la query puede traer toda la tabla --> |

---

# Historial de Cambios Importantes

<!-- Los agentes añaden entradas aquí tras modificaciones estructurales -->

<!--
- [2025-01-20] Renombrado UserService → AuthService para separar autenticación de gestión de usuarios.
- [2025-01-18] Añadido módulo notifications. Registrado en app/config.py.
-->
