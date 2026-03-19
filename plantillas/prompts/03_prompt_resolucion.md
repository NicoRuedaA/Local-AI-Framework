Analiza metódicamente el código del INPUT en busca de bugs reales y riesgos latentes. Tu output será el input del Optimizador, así que debe ser exhaustivo y accionable.

## Proceso obligatorio para cada problema encontrado

**Paso 1 — Hipótesis**
Lista las 3 causas más probables del problema o riesgo, ordenadas de mayor a menor probabilidad.

**Paso 2 — Evidencia**
Cita el archivo y la línea exacta donde se manifiesta el problema. Si es un bug potencial, describe el escenario concreto que lo dispararía (ej: "si dos usuarios llaman a POST /votes/ simultáneamente con el mismo feature_request_id...").

**Paso 3 — Causa raíz**
Explica en 2-3 líneas por qué el código falla o fallaría. Sé técnico y específico.

**Paso 4 — Código corregido**
Entrega el archivo COMPLETO corregido en formato:
```python filename: ruta/del/archivo.py
No entregues solo el fragmento. El archivo completo.

**Paso 5 — Prevención**
Un patrón, decorador, validación o test que evitaría este tipo de error en el futuro.

## Categorías de bugs a buscar activamente

- **Concurrencia:** ¿Los votos usan `select_for_update()`? ¿Hay race conditions posibles?
- **Seguridad:** ¿IDOR? ¿Un usuario puede modificar objetos de otro? ¿Hay datos sensibles expuestos en serializers?
- **ORM Django:** ¿Hay queries N+1 en listados? ¿Se usan `select_related`/`prefetch_related` donde hace falta?
- **Celery:** ¿Las tasks son idempotentes? ¿Reintentan en caso de fallo? ¿Hay riesgo de enviar emails duplicados?
- **Validación:** ¿Los serializers validan unicidad? ¿Los endpoints verifican permisos por objeto (object-level permissions)?
- **Errores silenciosos:** ¿Hay `except` que tragan excepciones? ¿Hay `get()` sin manejo de `DoesNotExist`?

## Si el código no tiene bugs evidentes
No escribas "el código se ve bien". Busca y reporta los 3 riesgos latentes más importantes con su escenario de fallo específico.
