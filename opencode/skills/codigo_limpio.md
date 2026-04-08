# Convenciones Técnicas Obligatorias

Estas reglas aplican a TODO el código generado en cualquier proyecto, independientemente del lenguaje o framework. No son sugerencias.

## Código

- Escribe código modular y limpio siguiendo los principios de Clean Code.
- Aplica el principio de responsabilidad única (SRP): cada función/clase hace una sola cosa.
- Usa nombres descriptivos en el mismo idioma que el proyecto (inglés para código, español para comentarios si el usuario lo prefiere).
- No añadas comentarios obvios. Comenta únicamente la lógica no evidente.
- Incluye tipado estático siempre que el lenguaje lo permita (type hints en Python, TypeScript sobre JS, etc.).
- Maneja todos los errores de forma explícita: nada de `except: pass` ni errores silenciosos.
- No uses números o strings mágicos: extráelos como constantes con nombre descriptivo.

## Estructura de archivos

- Un módulo = una responsabilidad. Evita archivos "cajón de sastre".
- Separa la lógica de negocio de la capa de entrada/salida (CLI, API, base de datos).
- Los tests van en una carpeta `/tests` espejando la estructura de `/src`.

## Formato de entrega

- Entrega el código en bloques separados por archivo.
- Indica la ruta completa de cada archivo como encabezado antes del bloque de código.
- Si se necesita instalar dependencias, indícalas al inicio con el comando exacto.
- Al final de cada entrega incluye una sección breve "Cómo probarlo" con pasos exactos.

## Calidad

- El código debe funcionar sin modificaciones adicionales salvo la configuración del entorno.
- Incluye validación de inputs en todos los puntos de entrada (funciones públicas, endpoints, CLI).
- Prefiere la legibilidad sobre la brevedad cuando haya que elegir.
