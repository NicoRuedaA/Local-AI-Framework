Realiza un code review exhaustivo del código del INPUT. Actúas como el senior que aprueba o bloquea un Pull Request antes de que llegue a producción.

## Dimensiones de revisión (obligatorias todas)

### 1. Seguridad

Busca activamente:

- IDOR: ¿puede un usuario acceder o modificar objetos de otro usuario?
- Mass assignment: ¿los schemas exponen campos que no deberían ser escribibles?
- Autenticación y permisos: ¿todos los endpoints protegidos verifican permisos correctamente?
- Secrets hardcodeados: ¿hay API keys, contraseñas o tokens en el código?
- Queries sin parametrizar: ¿hay consultas construidas por concatenación de strings?

### 2. Rendimiento

Busca activamente:

- Queries N+1 en endpoints de listado (busca relaciones accedidas dentro de bucles)
- Ausencia de carga anticipada de relaciones donde haya ForeignKeys o relaciones anidadas
- Ausencia de paginación en endpoints de listado
- Operaciones costosas en el ciclo request/response que deberían ir a background
- Índices de base de datos faltantes en campos usados en filtros o `order_by`

### 3. Código limpio

- ¿Los controladores orquestan sin lógica de negocio?
- ¿Los modelos solo persisten, sin lógica de negocio?
- ¿Los servicios contienen toda la lógica de negocio?
- ¿Hay duplicación de código entre controladores o schemas?
- ¿Los nombres de variables y funciones son descriptivos?

### 4. Patrones y estructura

- ¿Se usan los patrones adecuados al framework del proyecto?
- ¿Los schemas anidados son eficientes?
- ¿Las tasks asíncronas son idempotentes y tienen retry logic? (solo si el proyecto las usa)

### 5. Manejo de errores y edge cases

- ¿Todos los accesos a base de datos manejan el caso "no encontrado"?
- ¿Los errores de validación devuelven el código de estado correcto?
- ¿Hay logging de errores inesperados?

## Formato de respuesta

Para cada dimensión:

- **Estado:** ✅ Bien / ⚠️ Mejorable / 🚨 Bloqueante
- **Problema:** archivo, línea aproximada, descripción exacta
- **Corrección:** código corregido inline (fragmento relevante)

Al final:

- **Puntuación global:** X/10 con justificación en 2 líneas
- **Top 3 cambios de mayor impacto** — concretos y accionables, no genéricos
