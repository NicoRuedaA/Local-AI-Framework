# Idea del Proyecto

## ¿Qué quiero construir?

"Nexo" es una plataforma web para la gestión centralizada de feedback de usuarios y roadmap de productos. Permite a los usuarios sugerir nuevas funcionalidades, votar por sus favoritas y dejar comentarios, mientras que los administradores pueden priorizar estas solicitudes y actualizar su estado (ej. "Planeado", "Completado") para mantener a la comunidad informada sobre el progreso del producto.

## Usuarios objetivo

Equipos de desarrollo y Product Managers que necesitan priorizar su trabajo basados en datos reales, y los usuarios finales de sus productos que desean que sus peticiones sean escuchadas y organizadas.

## Requisitos funcionales

Autenticación y autorización de usuarios con diferenciación estricta de roles (Usuario estándar vs. Administrador/Staff).

Creación, edición, categorización (etiquetas/tags) y búsqueda de publicaciones (Feature Requests).

Sistema de votación (Upvoting) robusto que impida votos duplicados de un mismo usuario y gestione la concurrencia de forma segura.

Sistema de comentarios anidados (recursivos) dentro de cada publicación.

Capacidad para que los administradores cambien el "Estado" de una publicación ("Bajo revisión", "Planeado", "En desarrollo", "Lanzado").

Tarea en segundo plano que envíe notificaciones por correo electrónico a todos los usuarios que votaron por una propuesta cuando su estado pase a "Lanzado".

## Restricciones técnicas

Lenguaje/Framework: Python 3.11+ con Django 5.x y Django REST Framework (DRF) para exponer la API.

Base de datos: PostgreSQL (ideal para probar concurrencia y transacciones en los votos) o SQLite (aceptable para la fase inicial de desarrollo local).

Plataforma: Backend enfocado en API REST, con un panel de administración nativo de Django altamente customizado.

Otras restricciones: Uso de Celery + Redis para la gestión de tareas asíncronas (envío de emails).

## Lo que NO debe hacer

No debe incluir pasarelas de pago, facturación o gestión de planes SaaS.

No necesita chat en tiempo real ni WebSockets en esta primera iteración.

No requiere la configuración de un framework frontend complejo (como React, Angular o Vue); la evaluación se centrará puramente en la arquitectura del backend, el ORM de Django y la API.
