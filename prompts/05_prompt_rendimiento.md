Refactoriza el proyecto completo del INPUT aplicando todas las correcciones del reporte del Crítico y todas las mejoras de rendimiento y clean code que identifiques.

## Prioridad de trabajo

**Primero — Ítems BLOQUEANTES del reporte del Crítico**
Resuelve todos los problemas marcados como 🚨 Bloqueante antes de cualquier otra mejora. Sin excepciones.

**Segundo — Ítems Mejorables del reporte del Crítico**
Aplica todos los ⚠️ Mejorable del reporte. Si hay un conflicto entre el reporte y tu criterio, aplica el reporte y documenta el conflicto en la tabla de cambios.

**Tercero — Mejoras propias**
Una vez resuelto lo anterior, aplica las mejoras de rendimiento y clean code que identifiques por tu cuenta.

## Reglas absolutas

**REGLA 1 — COMPLETITUD:** Entrega el proyecto COMPLETO refactorizado. Todos los archivos, en el mismo orden que el Constructor. Prohibido entregar solo los archivos modificados.

**REGLA 2 — FORMATO:** Cada archivo precedido de su ruta:

```[lenguaje] filename: ruta/del/archivo.[ext]

**REGLA 3 — NO ROMPER CONTRATOS:** El comportamiento externo no cambia. Mismos endpoints, mismas respuestas, misma lógica de negocio. Si un cambio del Crítico implica modificar el contrato de la API, señálalo explícitamente antes de hacerlo.

**REGLA 4 — OPTIMIZACIONES PRIORITARIAS (adaptar al stack del proyecto):**
- Carga anticipada de relaciones en todos los endpoints con datos anidados
- Operaciones atómicas sobre campos numéricos usando expresiones del ORM
- Paginación donde falte
- Tasks asíncronas con reintentos (solo si el proyecto las usa)
- Índices en campos usados frecuentemente en filtros

## Estructura de respuesta

1. **Código refactorizado completo** (todos los archivos)
2. **Tabla de cambios:**
   | Archivo | Qué cambié | Por qué | Impacto esperado |
3. **Checklist del reporte del Crítico:**
   Lista cada ítem con ✅ Resuelto / ⚠️ Parcial / ❌ No aplicado (con justificación)
4. **Mejoras de rendimiento propias:**
   Complejidad antes vs después donde sea medible
```
