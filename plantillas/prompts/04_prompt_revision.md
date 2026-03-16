Revisa el código proporcionado en el INPUT. Analiza cada una de estas dimensiones:

1. Seguridad: ¿Hay vulnerabilidades? (inyección SQL, XSS, exposición de datos sensibles, secrets hardcodeados, etc.).
2. Rendimiento: ¿Hay cuellos de botella? (queries N+1, operaciones O(n²), cargas innecesarias...).
3. Código limpio: ¿Cumple con el principio de responsabilidad única? ¿Los nombres son descriptivos? ¿Hay duplicación?.
4. Patrones y estructura: ¿Usa patrones adecuados? ¿La estructura es coherente con el framework?
5. Manejo de errores: ¿Gestiona los edge cases? ¿Los errores se manejan o se tragan silenciosamente?

## Formato de respuesta
Para cada dimensión:
- Estado: Bien / Mejorable / Problema.
- Si hay problema: explica qué, dónde y muestra el código corregido.

Al final, da una puntuación global de 1 a 10 con un resumen de una línea. Cierra con los 3 cambios de mayor impacto que harías si solo pudieras cambiar 3 cosas.