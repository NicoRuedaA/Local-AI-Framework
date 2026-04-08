Genera la documentación técnica COMPLETA del proyecto del INPUT. La documentación debe ser tan buena que un desarrollador externo pueda levantar el proyecto y contribuir sin preguntarle nada a nadie.

## Archivos a entregar

### README.md principal
```markdown filename: README.md

Estructura obligatoria:
1. **Descripción** — Qué es el proyecto, qué problema resuelve, para quién es. Máximo 3 frases. Sin marketing.
2. **Arquitectura** — Diagrama en texto (ASCII) de los componentes del sistema y cómo se comunican.
3. **Requisitos previos** — Versiones exactas de todas las tecnologías necesarias.
4. **Instalación** — Comandos copy-paste, en orden, que funcionan en una terminal limpia:
   - Clonar repo
   - Crear entorno virtual o instalar dependencias
   - Configurar variables de entorno
   - Inicializar base de datos
   - Levantar servicios auxiliares (si los hay)
   - Levantar el servidor
5. **Variables de entorno** — Tabla completa: Variable | Descripción | Ejemplo | Obligatoria
6. **Cómo ejecutar los tests** — Comando exacto + cómo ver el reporte de cobertura
7. **Estructura del proyecto** — Árbol completo con descripción de cada carpeta y archivo relevante
8. **Documentación de la API** — Para cada endpoint:
   - Método + Ruta
   - Descripción en una línea
   - Autenticación requerida
   - Request body (ejemplo)
   - Response exitosa (ejemplo con código de estado)
   - Errores posibles (código + mensaje)
9. **Guía de contribución** — Cómo crear una rama, convenciones de commits, cómo ejecutar tests antes de un PR

### Docstrings inline
Añade docstrings al estilo estándar del lenguaje del proyecto a todas las funciones públicas de los servicios:
- Una línea de resumen
- Parámetros con tipo y descripción
- Valor de retorno con tipo y descripción
- Excepciones que puede lanzar
- Ejemplo de uso

### Guía de despliegue
```markdown filename: docs/DEPLOYMENT.md

- Configuración de la base de datos en producción
- Variables de entorno de producción (qué cambiar respecto a desarrollo)
- Configuración de servicios auxiliares en producción (si los hay)
- Checklist pre-despliegue
