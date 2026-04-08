Diseña la arquitectura técnica COMPLETA para el proyecto descrito en el INPUT. Este documento será la única referencia que usará el Constructor para generar el código, así que debe ser exhaustivo y sin ambigüedades. Guardalo en un archivo arquitectura.md

## INPUT

El proyecto a diseñar está descrito ÚNICAMENTE en el archivo
`idea_inicial.md`.
Ignora cualquier contenido de `context.md` que haga referencia
a proyectos anteriores — ese historial no aplica a este diseño.

## Entrega obligatoria

### 1. Stack tecnológico

Por cada tecnología: nombre, versión exacta, y justificación en una línea. Usa EXACTAMENTE las tecnologías que especifica `idea_inicial.md`. Solo propones alternativas si hay una razón técnica crítica, y la señalas explícitamente.

### 2. Estructura de carpetas COMPLETA

Árbol de archivos con TODOS los archivos que el Constructor deberá crear. Sin omisiones. Incluye archivos de configuración, entrada, dependencias, tests y fixtures.

**Regla de arquitectura — un modelo, una ubicación:** Cada modelo/entidad vive en el archivo de su módulo. NO incluyas definiciones de modelos en el archivo raíz del proyecto. Si debe existir, estará vacío.

### 3. Modelo de datos detallado

Para cada entidad/modelo:

- Nombre de la clase
- Todos los campos con su tipo exacto según el ORM/framework del proyecto
- Para campos con valores acotados (enums/choices): usa el mecanismo del framework y especifica el tamaño máximo calculado sobre el valor almacenado más largo + margen
- Índices necesarios
- Restricciones de unicidad a nivel de base de datos — **nunca solo a nivel de aplicación**
- El método de representación textual (`__str__` o equivalente) siempre
- **Nunca** un override del método de guardado solo para gestionar timestamps

**Regla obligatoria sobre el modelo de usuario:** Si el proyecto define un modelo de usuario custom:

- Configura explícitamente el sistema para usarlo
- Indica que todas las relaciones al usuario deben usar la referencia indirecta, no la clase directamente

### 4. Diseño de la API REST

Para cada endpoint:

- Método HTTP + ruta
- Permisos requeridos (anónimo / autenticado / solo admin)
- Qué hace en una línea
- Patrón de controlador recomendado (según el framework del proyecto)

### 5. Flujo de datos críticos

Describe paso a paso los flujos más complejos del sistema. Formato: Paso 1 → Paso 2 → ...

Si el proyecto usa operaciones concurrentes, especifica:

- Qué operación requiere bloqueo
- Que ese bloqueo debe estar dentro de una transacción explícita
- Qué garantía de unicidad existe a nivel de base de datos

Si el proyecto usa tareas asíncronas, especifica:

- Qué tecnología gestiona las tasks (según `idea_inicial.md`)
- Dónde se disparan (desde el controlador, no desde servicios)
- Cómo garantizan idempotencia

### 6. Decisiones de diseño

Las 5 decisiones arquitectónicas más importantes con su justificación, derivadas exclusivamente de los requisitos del proyecto.

### 7. Riesgos técnicos

3 riesgos concretos con su mitigación específica. Nada genérico — di exactamente qué query, qué endpoint, qué volumen.

### 8. Configuración principal

Especifica el contenido exacto de las secciones críticas de la configuración:

- Registro del modelo de usuario custom (si aplica)
- Lista de módulos/apps registrados
- Configuración de autenticación, paginación y permisos por defecto
- Configuración de servicios externos SOLO si el proyecto los usa

### 9. Archivo convenciones_proyecto.md

**Esta sección es obligatoria.** Genera el contenido completo del archivo
`convenciones_proyecto.md` rellenando
la plantilla de `/plantillas/skills/convenciones.md` con los valores
concretos de este proyecto:

- `{NOMBRE_PROYECTO}` → nombre real del proyecto
- `{STACK_DEL_PROYECTO}` → lista exacta de tecnologías con versiones (solo las que usa este proyecto)
- `{ARQUITECTURA_DE_CAPAS}` → diagrama de capas adaptado (omite las que no aplican)
- `{INTEGRACIONES_ASINCRONAS}` → convenciones específicas si el proyecto usa tasks, o: "Este proyecto no usa tareas asíncronas. No generar archivos de tasks ni configuración de brokers."

El Constructor usará `convenciones_proyecto.md` como su fuente de verdad, no la plantilla genérica.
