Analiza metódicamente el código del INPUT en busca de bugs reales y riesgos latentes. Tu output será el input del Optimizador, así que debe ser exhaustivo y accionable.

## Proceso obligatorio para cada problema encontrado

**Paso 1 — Hipótesis**
Lista las 3 causas más probables del problema o riesgo, ordenadas de mayor a menor probabilidad.

**Paso 2 — Evidencia**
Cita el archivo y la línea exacta donde se manifiesta el problema. Si es un bug potencial, describe el escenario concreto que lo dispararía.

**Paso 3 — Causa raíz**
Explica en 2-3 líneas por qué el código falla o fallaría. Sé técnico y específico.

**Paso 4 — Código corregido**
Entrega el archivo COMPLETO corregido en formato:

```[lenguaje] filename: ruta/del/archivo.[ext]
No entregues solo el fragmento. El archivo completo.

**Paso 5 — Prevención**
Un patrón, validación o test que evitaría este tipo de error en el futuro.

## Categorías de bugs a buscar activamente

- **Concurrencia:** ¿Las operaciones críticas usan bloqueo dentro de una transacción? ¿Hay race conditions posibles?
- **Seguridad:** ¿IDOR? ¿Un usuario puede acceder o modificar objetos de otro? ¿Hay datos sensibles expuestos?
- **Rendimiento:** ¿Hay queries N+1 en listados? ¿Se cargan relaciones de forma eficiente?
- **Tareas asíncronas (si el proyecto las usa):** ¿Las tasks son idempotentes? ¿Reintentan en caso de fallo?
- **Validación:** ¿Los schemas/serializers validan unicidad? ¿Los endpoints verifican permisos por objeto?
- **Errores silenciosos:** ¿Hay bloques `except` que tragan excepciones? ¿Hay consultas sin manejo de "no encontrado"?
- **Imports faltantes:** Para cada archivo, ¿cada símbolo usado tiene su import en ese mismo archivo?

## Si el código no tiene bugs evidentes
No escribas "el código se ve bien". Busca y reporta los 3 riesgos latentes más importantes con su escenario de fallo específico.
```
