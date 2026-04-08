---
name: unity-mcp
description: Patrones y convenciones para trabajar con el Unity Editor via MCP for Unity. Úsala cuando vayas a crear o modificar GameObjects, scripts, escenas o assets en Unity.
---

# Unity MCP Workflow

## Principios clave

- **Optimización de llamadas:** Usa `batch_execute` siempre que hagas múltiples operaciones — es 10-100x más rápido que hacer llamadas individuales.
- **Contexto primero:** Antes de crear GameObjects, consulta el recurso `editor_selection` para entender el contexto actual del usuario.
- **Validación de API:** Usa `unity_reflect` para verificar la existencia de APIs y componentes de C# antes de escribir código a ciegas.
- **Recarga de dominio (Domain Reload):** Ten en cuenta que Unity necesita compilar después de crear/modificar scripts. NO intentes adjuntar un script a un GameObject inmediatamente después de crearlo; verifica primero que ha compilado correctamente.

## Flujo para crear y modificar scripts

1. `unity_reflect` — Verifica que las clases/métodos que vas a usar existen en la versión actual de Unity.
2. `create_script` (o edición) — Escribe o modifica el archivo.
3. `read_console` — Lee la consola para asegurarte de que la recarga de dominio terminó sin errores de sintaxis.
4. `validate_script` — Comprueba la lógica.
5. **Resolución:** Si hay errores, corrígelos inmediatamente antes de pasar a otra tarea.

## Flujo para modificar escenas

1. `manage_scene` (action: `get`) — Entiende la jerarquía y el estado actual.
2. `batch_execute` — Agrupa todas las operaciones de instanciación, movimiento y configuración en una sola llamada.
3. `read_console` — Verifica el resultado y detecta advertencias.
4. `manage_scene` (action: `save`) — Guarda la escena para no perder los cambios.

## Convenciones de Código C# y Unity

- **Clases y Estructuras:** `PascalCase` (`PlayerController`, `HexGrid`).
- **Métodos (Públicos y Privados):** `PascalCase` (`MovePlayer`, `CalculatePath`).
- **Campos Privados:** `_camelCase` (`_moveSpeed`, `_health`).
- **Variables Expuestas:** Usa `[SerializeField] private` en lugar de `public` para variables que se asignan desde el Inspector.
- **Variables Locales y Parámetros:** `camelCase` (`currentSpeed`, `targetPosition`).
- **Rendimiento:** - Evita `Update()` para lógica que no requiere ejecutarse cada frame. Usa Coroutines, `InvokeRepeating`, o eventos.
  - NUNCA uses `GetComponent<T>()` o `Find()` dentro de `Update()`. Cachéalo en `Awake()` o `Start()`.

## Convenciones de Proyecto

Mantén el proyecto organizado usando la estructura de carpetas estándar:

- Scripts en `Assets/Scripts/` (agrupados por subcarpetas funcionales si es necesario).
- Prefabs en `Assets/Prefabs/`.
- Materiales en `Assets/Materials/`.
- Sprites/Modelos en `Assets/Art/`.
