mi_entorno_ia/
│
├── iniciar_entorno.py            # 🏗️ Script para crear estas carpetas automáticamente.
├── orquestador.py                # 🧠 EL CEREBRO: El script que conecta LM Studio con tus archivos.
├── index.md                      # 🗺️ EL MAPA: Le explica a la IA cómo moverse por estas carpetas.
│
├── 📁 plantillas/                # ⚙️ EL MOTOR (Intocable. Basado en los 7 pasos de tu PDF)
│   │
│   ├── 📁 agents/                # 🎭 LAS PERSONALIDADES (System Prompts)
│   │   ├── 01_arquitecto.md      # "Actúa como un arquitecto senior..."
│   │   ├── 02_constructor.md     # "Actúa como un desarrollador senior..."
│   │   ├── 03_detective.md       # "Actúa como un debugger experto..."
│   │   ├── 04_critico.md         # "Actúa como un code reviewer..."
│   │   ├── 05_optimizador.md     # "Actúa como ingeniero de rendimiento..."
│   │   ├── 06_escudo.md          # "Actúa como ingeniero de QA..."
│   │   └── 07_narrador.md        # "Actúa como technical writer..."
│   │
│   ├── 📁 prompts/               # 🎯 LAS TAREAS (User Prompts)
│   │   ├── 01_planificacion.md   # "Diseña la arquitectura para..."
│   │   ├── 02_generacion.md      # "Implementa lo siguiente..."
│   │   ├── 03_resolucion.md      # "Analiza este problema metódicamente..."
│   │   ├── 04_revision.md        # "Revisa este código evaluando seguridad..."
│   │   ├── 05_rendimiento.md     # "Refactoriza este código..."
│   │   ├── 06_cobertura.md       # "Escribe una suite de tests..."
│   │   └── 07_tecnica.md         # "Genera documentación completa..."
│   │
│   └── 📁 skills/                # 🛠️ LAS REGLAS
│       └── convenciones.md       # Ej: "Usa Python 3.10, tipado estricto, documenta en español"
│
└── 📁 mi_proyecto_actual/        # 💾 LA MEMORIA (Donde se guarda el trabajo real)
    │
    ├── 📁 01_spec/               # El contexto de lo que estamos construyendo
    │   ├── idea_inicial.md       # Lo ÚNICO que escribes tú (ej: "Quiero una app del clima")
    │   └── arquitectura.md       # Archivo generado por la IA tras ejecutar el Paso 1.
    │
    └── 📁 src/                   # El código fuente
        ├── codigo_generado.py    # Archivos generados por la IA tras ejecutar el Paso 2.
        └── README.md             # Generado por la IA tras ejecutar el Paso 7.
