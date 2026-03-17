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
├── iniciar_entorno.py            # 🏗️ Script de inicialización rápida.
├── orquestador.py                # 🧠 EL CEREBRO: Conecta la IA con los archivos locales.
├── index.md                      # 🗺️ EL MAPA: Contexto global para que la IA no se pierda.
│
├── 📁 plantillas/                # ⚙️ EL MOTOR (Estático y Reutilizable)
│   ├── 📁 agents/                # 🎭 System Prompts: Define quién es la IA (Arquitecto, Constructor...)
│   │   ├── 01_arquitecto.md      # "Actúa como un arquitecto senior..."
│   │   ├── 02_constructor.md     # "Actúa como un desarrollador senior..."
│   │   ├── 03_detective.md       # "Actúa como un debugger experto..."
│   │   ├── 04_critico.md         # "Actúa como un code reviewer..."
│   │   ├── 05_optimizador.md     # "Actúa como ingeniero de rendimiento..."
│   │   ├── 06_escudo.md          # "Actúa como ingeniero de QA..."
│   │   └── 07_narrador.md        # "Actúa como technical writer..."
│   ├── 📁 prompts/               # 🎯 User Prompts: Define qué debe hacer (Diseñar, Programar, Testear...)
│   │   ├── 01_planificacion.md   # "Diseña la arquitectura para..."
│   │   ├── 02_generacion.md      # "Implementa lo siguiente..."
│   │   ├── 03_resolucion.md      # "Analiza este problema metódicamente..."
│   │   ├── 04_revision.md        # "Revisa este código evaluando seguridad..."
│   │   ├── 05_rendimiento.md     # "Refactoriza este código..."
│   │   ├── 06_cobertura.md       # "Escribe una suite de tests..."
│   │   └── 07_tecnica.md         # "Genera documentación completa..."
│   └── 📁 skills/                # 🛠️ Reglas técnicas globales (Convenciones, lenguajes, etc.)
│       └── convenciones.md       # Ej: "Usa Python 3.10, tipado estricto, documenta en español"
│
└── 📁 mi_proyecto_actual/        # 💾 LA MEMORIA (Dinámico y Específico del proyecto)
    ├── 📁 01_spec/               # Entradas y planes (idea_inicial.md, arquitectura.md)
    │   ├── idea_inicial.md       # Lo ÚNICO que escribes tú (ej: "Quiero una app del clima")
    │   └── arquitectura.md       # Archivo generado por la IA tras ejecutar el Paso 1.
    └── 📁 src/                   # Salidas (Código fuente generado por la IA)
        ├── codigo_generado.py    # Archivos generados por la IA tras ejecutar el Paso 2.
        └── README.md             # Generado por la IA tras ejecutar el Paso 7.
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
