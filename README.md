# 🤖 Agencia de Desarrollo IA (Local & Autónoma)

Framework ligero para orquestar modelos de lenguaje locales como agentes autónomos de desarrollo de software. Cada "agente" tiene un rol especializado (arquitecto, constructor, debugger, etc.) y trabaja en secuencia sobre tu proyecto.

---

## Requisitos

- Python 3.10+
- [LM Studio](https://lmstudio.ai/) con el servidor local activo en el puerto `1234`
- Cualquier modelo de código descargado en LM Studio (recomendado: DeepSeek Coder, Qwen2.5-Coder o similar)

```bash
pip install openai
```

---

## Inicio rápido

```bash
# 1. Genera la estructura de carpetas (solo la primera vez)
python iniciar_entorno.py

# 2. Escribe tu idea en:
#    mi_proyecto_actual/01_spec/idea_inicial.md

# 3. Ejecuta el pipeline completo (modo automático, sin confirmaciones)
python orquestador.py --auto

# O ejecuta paso a paso con confirmación antes de guardar cada archivo
python orquestador.py 1
python orquestador.py 2
# ...
```

---

## Flujo del pipeline

```
idea_inicial.md
      │
      ▼
 [Paso 1] Arquitecto   →  01_arquitectura.md
      │
      ▼
 [Paso 2] Constructor  →  02_codigo_generado.md
      │
      ▼
 [Paso 3] Detective    →  03_codigo_corregido.md
      │
      ├──▶ [Paso 4] Crítico      →  04_reporte_revision.md
      │
      ▼
 [Paso 5] Optimizador  →  05_codigo_refactorizado.md
      │
      ├──▶ [Paso 6] Escudo       →  06_tests.md
      │
      └──▶ [Paso 7] Narrador     →  README.md (del proyecto)
```

Cada paso encadena el output del anterior como input, excepto el 4 (revisión) que trabaja sobre el código corregido del paso 3 de forma independiente.

---

## Comandos disponibles

| Comando | Descripción |
|---|---|
| `python orquestador.py 1` | Ejecuta solo el paso 1 (con confirmación) |
| `python orquestador.py --auto` | Ejecuta los 7 pasos sin confirmaciones |
| `python orquestador.py --status` | Muestra qué archivos de output ya existen |
| `python orquestador.py --help` | Muestra la ayuda |

---

## Estructura del proyecto

```
proyecto/
│
├── orquestador.py              # 🧠 El cerebro: conecta la IA con los archivos
├── iniciar_entorno.py          # 🏗️ Crea la estructura de carpetas inicial
├── index.md                    # 🗺️ Contexto global que lee la IA en cada paso
│
├── plantillas/                 # ⚙️ Motor (estático, no tocar)
│   ├── agents/                 # 🎭 Roles de IA (quién actúa)
│   ├── prompts/                # 🎯 Tareas de IA (qué hace)
│   └── skills/                 # 🛠️ Convenciones técnicas globales
│
└── mi_proyecto_actual/         # 💾 Memoria (específico de tu proyecto)
    ├── 01_spec/                # Idea inicial + arquitectura generada
    └── src/                    # Código y documentación generados
```

---

## Personalización

Para adaptar el framework a un nuevo proyecto:

1. Edita `mi_proyecto_actual/01_spec/idea_inicial.md` con tu nueva idea.
2. Borra los archivos de output anteriores en `mi_proyecto_actual/src/` y `01_spec/01_arquitectura.md`.
3. Ejecuta `python orquestador.py --auto` o paso a paso.

Para cambiar las reglas técnicas globales (lenguaje, framework, estilo de código), edita `plantillas/skills/convenciones.md`.

---

## Solución de problemas

**Error de conexión con LM Studio**
- Abre LM Studio → pestaña "Local Server" → pulsa "Start Server"
- Activa la opción "Enable CORS"
- Verifica que el puerto es `1234`

**El paso N falla porque no encuentra el input**
- Asegúrate de haber ejecutado los pasos anteriores en orden
- Usa `python orquestador.py --status` para ver qué archivos faltan
