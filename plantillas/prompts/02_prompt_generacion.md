Implementa el proyecto COMPLETO según la arquitectura definida en el INPUT. Este es el paso más importante del pipeline: el código que entregues debe poder ejecutarse sin modificaciones.

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

**REGLA 5 — IMPORTS:** Cada archivo importa todo lo que usa. Un símbolo importado en otro archivo del proyecto NO está disponible en el archivo actual. Revisa cada archivo de forma completamente independiente antes de entregarlo.

**REGLA 6 — DEPENDENCIAS:** El archivo de dependencias del proyecto incluye versiones fijadas para todas las dependencias directas.

## Al final de todos los archivos
Incluye una sección "Cómo ejecutar el proyecto" con los comandos exactos y en orden:
1. Instalar dependencias
2. Configurar variables de entorno
3. Preparar la base de datos (migraciones, seeds, scripts de inicialización)
4. Levantar servicios auxiliares necesarios (colas, caché, etc.)
5. Levantar el servidor o ejecutar el proyecto
6. Verificar que funciona (endpoint o comando de comprobación)
