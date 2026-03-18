# Convenciones Técnicas

## Código

- Escribe funciones pequeñas con un único nivel de abstracción y una sola responsabilidad (SRP).
- Usa nombres que revelen la intención. Sin abreviaturas crípticas. Idioma: inglés para código, español para comentarios de lógica no evidente.
- No comentarás lo obvio: solo la lógica que no se explica sola con el nombre.
- Incluye tipado estático siempre que el lenguaje lo permita (type hints en Python, TypeScript sobre JS). Prohibido `any` u `Object` salvo causa justificada.
- Maneja todos los errores de forma explícita. Prohibido `except: pass` y errores silenciosos.
- Extrae todo valor literal a una constante con nombre descriptivo (clase `Constants` o `Enum`). Prohibidos los números y strings mágicos.

## Arquitectura y Diseño

Aplica SOLID como guía de diseño:

- **SRP / Módulos**: Un archivo, una responsabilidad. Evita archivos "cajón de sastre".
- **OCP**: Diseña para extender mediante polimorfismo o composición, sin tocar el código existente.
- **ISP**: Prefiere interfaces específicas sobre interfaces generalistas. No obligues a implementar métodos que no se usan.
- **DIP**: La lógica de negocio no depende de detalles de infraestructura. Usa interfaces/abstracciones para desacoplar dominio de base de datos, APIs externas, etc.

Aplica patrones de diseño clásicos (Factory, Strategy, Observer) cuando la complejidad lo justifique y simplifiquen estructuras `if/else` o `switch` excesivas.

## Estructura de Archivos

- Separa radicalmente la lógica de negocio (dominio/servicios) de la capa de persistencia y de la interfaz (CLI/Web/API).
- La estructura de `/tests` debe ser un espejo de `/src`.

## Calidad

- El código entregado debe funcionar sin modificaciones salvo configuración de entorno.
- Valida los inputs en todos los puntos de entrada: funciones públicas, endpoints, CLI.
- Prioriza legibilidad sobre brevedad cuando tengas que elegir.

## Entrega

-
