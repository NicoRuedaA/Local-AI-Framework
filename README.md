# 🤖 Local AI Framework

Framework ligero para orquestar modelos de lenguaje locales y en la nube como agentes autónomos de desarrollo de software. Cada agente tiene un rol especializado y trabaja en secuencia sobre tu proyecto, encadenando su output como input del siguiente.

---

## Requisitos

- Python 3.10+
- [LM Studio](https://lmstudio.ai/) con el servidor local activo en el puerto `1234`
- Modelos descargados en LM Studio (recomendado: Qwen2.5-Coder 32b y 7b)
- *(Opcional)* API key de [Google AI Studio](https://aistudio.google.com/) para usar Gemini

```bash
pip install openai
```

---

## Inicio rápido

```bash
# 1. Genera la estructura de carpetas (solo la primera vez)
py setup.py

# 2. Escribe tu idea en:
#    mi_proyecto_actual/01_spec/idea_inicial.md

# 3. Configura tu stack en:
#    plantillas/skills/convenciones.md

# 4. Ejecuta el pipeline completo
py orquestador.py --auto

# O paso a paso con confirmación antes de guardar cada archivo
py orquestador.py 1
py orquestador.py 2
# ...
```

> **Nota Windows:** usa `py` en lugar de `python`. Si `python` no responde, es el alias de la Microsoft Store.

---

## Flujo del pipeline

```
idea_inicial.md
      │
      ▼
 [Paso 1] Arquitecto      →  01_arquitectura.md
      │
      ▼
 [Paso 2] Constructor     →  02_codigo_generado.md  +  archivos individuales en src/
      │
      ▼
 [Paso 2.5] Reparador     →  02.5_codigo_reparado.md   ← se omite si no hay errores
      │
      ▼
 [Paso 3] Detective       →  03_codigo_corregido.md
      │
      ├──▶ [Paso 4] Crítico       →  04_reporte_revision.md
      │              │
      │              └──────────────────────────────────────┐
      ▼                                                      ▼
 [Paso 5] Optimizador     →  05_codigo_refactorizado.md  ← recibe código + reporte del Crítico
      │
      ├──▶ [Paso 6] Escudo        →  06_tests.md
      │
      └──▶ [Paso 7] Narrador      →  README.md del proyecto
```

El Optimizador (paso 5) recibe tanto el código corregido del paso 3 como el reporte de revisión del Crítico (paso 4), aplicando todos los cambios marcados como bloqueantes o mejorables antes de refactorizar.

---

## Comandos disponibles

| Comando | Descripción |
|---|---|
| `py orquestador.py 1` | Ejecuta solo el paso 1 (con confirmación) |
| `py orquestador.py 2.5` | Ejecuta el Reparador manualmente |
| `py orquestador.py --auto` | Ejecuta todos los pasos sin confirmaciones |
| `py orquestador.py --status` | Muestra qué archivos existen y el % completado |
| `py orquestador.py --context` | Muestra el historial de decisiones del proyecto |
| `py orquestador.py --help` | Muestra la ayuda completa |

---

## Configuración de modelos — `modelos.json`

Crea `modelos.json` en la raíz para asignar un proveedor y modelo distinto a cada agente. Si no existe, todos los agentes usarán LM Studio con el modelo `local-model`.

**Proveedores soportados:** `lmstudio` (local) · `gemini` (Google AI Studio)

```json
{
  "arquitecto":  {"proveedor": "gemini",   "modelo": "gemini-2.0-flash"},
  "constructor": {"proveedor": "lmstudio", "modelo": "qwen2.5-coder-32b-instruct"},
  "detective":   {"proveedor": "lmstudio", "modelo": "qwen2.5-coder-32b-instruct"},
  "critico":     {"proveedor": "gemini",   "modelo": "gemini-2.0-flash"},
  "optimizador": {"proveedor": "lmstudio", "modelo": "qwen2.5-coder-32b-instruct"},
  "escudo":      {"proveedor": "lmstudio", "modelo": "qwen2.5-coder-7b-instruct"},
  "narrador":    {"proveedor": "lmstudio", "modelo": "qwen2.5-coder-7b-instruct"}
}
```

Para usar Gemini, añade tu API key en un archivo `.env` en la raíz:

```
GEMINI_API_KEY=tu_clave_aqui
```

> El nombre exacto de los modelos en LM Studio aparece en la pestaña *Local Server*. Cópialo tal cual (ej: `qwen/qwen2.5-coder-32b@q4_k_m`).

---

## Validación automática — `validaciones.json`

El Reparador (paso 2.5) revisa el código generado y corrige errores antes de que lleguen al Detective. Las reglas de validación son específicas por lenguaje y se definen en archivos `.md` dentro de `plantillas/validators/`.

Crea `validaciones.json` en la raíz indicando qué validators aplican a tu proyecto:

```json
{
  "validators": [
    "plantillas/validators/python.md",
    "plantillas/validators/django.md"
  ]
}
```

**Validators incluidos:**

| Archivo | Cubre |
|---|---|
| `python.md` | Imports fusionados, símbolos sin importar, imports relativos en raíz, credenciales hardcodeadas |
| `django.md` | `select_for_update` sin transacción, `permission_classes` ausentes, `fields = '__all__'`, `AUTH_USER_MODEL`, paginación |
| `javascript.md` | `require`/`import` mezclados, promesas sin manejo de error, `var`, credenciales hardcodeadas |
| `fastapi.md` | Sesiones async, `Depends`, modelos Pydantic sin tipos, `response_model`, `HTTPException` |

Si no existe `validaciones.json` o no tiene validators, el paso 2.5 se omite automáticamente.

> Para añadir soporte a un nuevo lenguaje, crea `plantillas/validators/tu_lenguaje.md` con las reglas y añádelo al JSON.

---

## Estructura del proyecto

```
proyecto/
│
├── orquestador.py                # 🧠 El cerebro: conecta la IA con los archivos
├── setup.py                      # 🏗️ Inicialización del entorno (ejecutar solo una vez)
├── index.md                      # 🗺️ Contexto global inyectado en todos los pasos
├── modelos.json                  # ⚙️ Proveedor y modelo por agente
├── validaciones.json             # 🔍 Validators de código activos para este proyecto
├── .env                          # 🔑 GEMINI_API_KEY (nunca subir a git)
│
├── 📁 plantillas/                # Motor estático y reutilizable entre proyectos
│   ├── 📁 agents/                # System prompts: quién es cada agente
│   │   ├── 01_agente_arquitecto.md
│   │   ├── 02_agente_constructor.md
│   │   ├── 03_agente_detective.md
│   │   ├── 04_agente_critico.md
│   │   ├── 05_agente_optimizador.md
│   │   ├── 06_agente_escudo.md
│   │   └── 07_agente_narrador.md
│   ├── 📁 prompts/               # User prompts: qué debe entregar cada agente
│   │   ├── 01_prompt_planificacion.md
│   │   ├── 02_prompt_generacion.md
│   │   ├── 02.5_prompt_reparacion.md   # ← Reparador
│   │   ├── 03_prompt_resolucion.md
│   │   ├── 04_prompt_revision.md
│   │   ├── 05_prompt_rendimiento.md
│   │   ├── 06_prompt_cobertura.md
│   │   └── 07_prompt_tecnica.md
│   ├── 📁 skills/                # Convenciones técnicas del proyecto actual
│   │   └── convenciones.md       # Stack, idioma, estilo de código — editar por proyecto
│   └── 📁 validators/            # Reglas de validación por lenguaje/framework
│       ├── python.md
│       ├── django.md
│       ├── javascript.md
│       └── fastapi.md
│
└── 📁 mi_proyecto_actual/        # Memoria dinámica del proyecto en curso
    ├── context.md                # Historial acumulativo de decisiones (auto-generado)
    ├── 📁 01_spec/
    │   ├── idea_inicial.md       # Lo único que escribes tú
    │   └── 01_arquitectura.md    # Generado por el Arquitecto
    └── 📁 src/                   # Outputs del pipeline
        ├── 02_codigo_generado.md
        ├── 02.5_codigo_reparado.md
        ├── 03_codigo_corregido.md
        ├── 04_reporte_revision.md
        ├── 05_codigo_refactorizado.md
        ├── 06_tests.md
        ├── README.md
        └── [archivos .py/.js/... extraídos automáticamente]
```

---

## Personalización por proyecto

Para empezar un proyecto nuevo:

1. Edita `mi_proyecto_actual/01_spec/idea_inicial.md` con tu idea.
2. Edita `plantillas/skills/convenciones.md` con el stack del nuevo proyecto.
3. Actualiza `validaciones.json` con los validators del nuevo lenguaje.
4. Actualiza `modelos.json` si quieres usar modelos distintos.
5. Borra los outputs anteriores:
   ```bash
   # PowerShell
   Remove-Item mi_proyecto_actual\src\* -Recurse
   Remove-Item mi_proyecto_actual\01_spec\01_arquitectura.md
   Remove-Item mi_proyecto_actual\context.md
   ```
6. Lanza el pipeline: `py orquestador.py --auto`

---

## Memoria acumulativa

El orquestador guarda automáticamente un resumen de cada paso completado en `mi_proyecto_actual/context.md`. Este historial se inyecta en el contexto de todos los pasos siguientes para que los agentes no contradigan decisiones ya tomadas.

```bash
# Ver el historial completo
py orquestador.py --context
```

---

## Extracción multi-archivo

Si el Constructor genera bloques con la anotación de nombre de archivo, el orquestador los extrae automáticamente como archivos individuales en `src/`:

```python
# El Constructor debe generar bloques en este formato:
```python filename: nexo/features/models.py
# ... código ...
```

Para activarlo, añade esta instrucción a `plantillas/skills/convenciones.md`:

```
Cada archivo va precedido de su ruta completa:
```[lenguaje] filename: ruta/completa/del/archivo.[ext]
```

---

## Progreso en tiempo real

En modo `--auto` el orquestador muestra una barra de progreso con ETA calculada a partir de la media de los pasos ya completados:

```
  [████████████░░░░░░░░] 57%  —  4/7 pasos completados
  ⏱  Transcurrido: 18m 22s   |   ETA restante: 13m 45s
```

El comando `--status` muestra el estado con porcentaje y tamaño de cada archivo generado:

```bash
py orquestador.py --status
```

---

## Solución de problemas

**`python` no responde o termina sin output**
Usa `py` en Windows. Si tampoco funciona, ve a *Configuración → Aplicaciones → Alias de ejecución* y desactiva los alias de `python.exe`.

**Error: `No module named 'openai'`**
```bash
py -m pip install openai
```

**Error de modelo no encontrado en LM Studio**
El nombre del modelo debe coincidir exactamente con el identificador que aparece en LM Studio → *Local Server*. Cópialo desde ahí y pégalo en `modelos.json`.

**Error de conexión con LM Studio**
- Abre LM Studio → pestaña *Local Server* → pulsa *Start Server*
- Activa la opción *Enable CORS*
- Verifica que el puerto es `1234`

**Error de Gemini: API key no encontrada**
Crea un archivo `.env` en la raíz del proyecto con:
```
GEMINI_API_KEY=tu_clave_aqui
```

**El paso N falla porque no encuentra el input**
```bash
py orquestador.py --status   # ver qué archivos faltan
py orquestador.py 2          # relanzar solo el paso problemático
```
