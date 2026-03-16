# 🤖 Agencia de Desarrollo IA (Local & Autónoma)

Este repositorio contiene un framework ligero y potente para orquestar modelos de lenguaje locales como agentes autónomos de desarrollo de software. 

En lugar de copiar y pegar prompts manualmente, este sistema utiliza un **Script Orquestador** que coordina a diferentes "Agentes" (Personalidades) para que ejecuten "Tareas" (Prompts) de forma secuencial, escribiendo el código directamente en tu disco duro.

---

## 🏗️ Arquitectura del Sistema: Motor vs. Memoria

El diseño de este framework se basa en la **Separación de Responsabilidades**. El entorno está dividido en dos grandes bloques para maximizar la escalabilidad y reutilización:

```text
mi_entorno_ia/
│
├── iniciar_entorno.py            # 🏗️ Script de inicialización rápida.
├── orquestador.py                # 🧠 EL CEREBRO: Conecta la IA con los archivos locales.
├── index.md                      # 🗺️ EL MAPA: Contexto global para que la IA no se pierda.
│
├── 📁 plantillas/                # ⚙️ EL MOTOR (Estático y Reutilizable)
│   ├── 📁 agents/                # 🎭 System Prompts: Define quién es la IA (Arquitecto, Constructor...)
│   ├── 📁 prompts/               # 🎯 User Prompts: Define qué debe hacer (Diseñar, Programar, Testear...)
│   └── 📁 skills/                # 🛠️ Reglas técnicas globales (Convenciones, lenguajes, etc.)
│
└── 📁 mi_proyecto_actual/        # 💾 LA MEMORIA (Dinámico y Específico del proyecto)
    ├── 📁 01_spec/               # Entradas y planes (idea_inicial.md, arquitectura.md)
    └── 📁 src/                   # Salidas (Código fuente generado por la IA)
