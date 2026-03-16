import os
import sys
from openai import OpenAI

cliente = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Cada paso encadena el output del anterior como input
# temperature ajustada por tipo de tarea
FLUJO = {
    "1": {
        "nombre": "Planificación y Arquitectura",
        "agente": "plantillas/agents/01_agente_arquitecto.md",
        "prompt": "plantillas/prompts/01_prompt_planificacion.md",
        "input": "mi_proyecto_actual/01_spec/idea_inicial.md",
        "output": "mi_proyecto_actual/01_spec/01_arquitectura.md",
        "temperature": 0.3,
    },
    "2": {
        "nombre": "Generación de Código",
        "agente": "plantillas/agents/02_agente_constructor.md",
        "prompt": "plantillas/prompts/02_prompt_generacion.md",
        "input": "mi_proyecto_actual/01_spec/01_arquitectura.md",
        "output": "mi_proyecto_actual/src/02_codigo_generado.md",
        "temperature": 0.2,
    },
    "3": {
        "nombre": "Debugging (Detective)",
        "agente": "plantillas/agents/03_agente_detective.md",
        "prompt": "plantillas/prompts/03_prompt_resolucion.md",
        "input": "mi_proyecto_actual/src/02_codigo_generado.md",      # lee código original
        "output": "mi_proyecto_actual/src/03_codigo_corregido.md",
        "temperature": 0.1,
    },
    "4": {
        "nombre": "Code Review (Crítico)",
        "agente": "plantillas/agents/04_agente_critico.md",
        "prompt": "plantillas/prompts/04_prompt_revision.md",
        "input": "mi_proyecto_actual/src/03_codigo_corregido.md",     # lee código corregido
        "output": "mi_proyecto_actual/src/04_reporte_revision.md",
        "temperature": 0.2,
    },
    "5": {
        "nombre": "Refactoring (Optimizador)",
        "agente": "plantillas/agents/05_agente_optimizador.md",
        "prompt": "plantillas/prompts/05_prompt_rendimiento.md",
        "input": "mi_proyecto_actual/src/03_codigo_corregido.md",     # lee código corregido
        "output": "mi_proyecto_actual/src/05_codigo_refactorizado.md",
        "temperature": 0.2,
    },
    "6": {
        "nombre": "Testing (Escudo)",
        "agente": "plantillas/agents/06_agente_escudo.md",
        "prompt": "plantillas/prompts/06_prompt_cobertura.md",
        "input": "mi_proyecto_actual/src/05_codigo_refactorizado.md", # lee código refactorizado
        "output": "mi_proyecto_actual/src/06_tests.md",
        "temperature": 0.2,
    },
    "7": {
        "nombre": "Documentación (Narrador)",
        "agente": "plantillas/agents/07_agente_narrador.md",
        "prompt": "plantillas/prompts/07_prompt_tecnica.md",
        "input": "mi_proyecto_actual/src/05_codigo_refactorizado.md", # documenta el código final
        "output": "mi_proyecto_actual/src/README.md",
        "temperature": 0.5,  # más alto para prosa más natural
    },
}


def leer_archivo(ruta: str) -> str:
    """Lee un archivo. Si no existe, devuelve advertencia en lugar de romper el script."""
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read().strip()
    return f"[Aviso: No se encontró información en {ruta}. Revisa la ruta o genera el paso anterior primero.]"


def guardar_archivo(ruta: str, contenido: str) -> None:
    """Guarda el archivo en la ruta especificada, creando directorios si hacen falta."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"\n✅ Guardado en: {ruta}")


def ejecutar_paso(paso: str, auto: bool = False) -> bool:
    """
    Ejecuta un paso del flujo. Devuelve True si se guardó el resultado, False si se canceló.
    El flag `auto` omite la confirmación interactiva.
    """
    if paso not in FLUJO:
        print(f"❌ Error: El paso '{paso}' no existe. Usa un número del 1 al 7.")
        return False

    config = FLUJO[paso]
    print(f"\n{'='*55}")
    print(f"🚀  Paso {paso}/7 — {config['nombre']}")
    print(f"{'='*55}")
    print(f"   📥 Input : {config['input']}")
    print(f"   📤 Output: {config['output']}")

    contexto_global = leer_archivo("index.md")
    skills = leer_archivo("plantillas/skills/convenciones.md")

    system_prompt = f"""{contexto_global}

=== TU ROL PARA ESTA TAREA ===
{leer_archivo(config['agente'])}

=== CONVENCIONES TÉCNICAS (SKILLS) ===
{skills}
"""

    user_prompt = f"""=== ESTADO ACTUAL DEL PROYECTO (INPUT) ===
{leer_archivo(config['input'])}

=== TU TAREA ACTUAL ===
{leer_archivo(config['prompt'])}
"""

    print("\n🧠 Consultando modelo... (puede tardar unos segundos)\n")

    try:
        respuesta = cliente.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=config["temperature"],
        )

        resultado = respuesta.choices[0].message.content

        print("=" * 55)
        print(f"✨  RESPUESTA — {config['nombre']}")
        print("=" * 55)
        preview = resultado[:800]
        print(preview + ("\n\n... [truncado para previsualización]" if len(resultado) > 800 else ""))
        print("=" * 55)

        if auto:
            guardar_archivo(config["output"], resultado)
            print(f"🎉 Paso {paso} completado (modo automático).")
            return True

        confirmacion = input(f"\n¿Guardar en '{config['output']}'? (s/n): ").strip().lower()
        if confirmacion == "s":
            guardar_archivo(config["output"], resultado)
            print(f"🎉 Paso {paso} completado.")
            return True
        else:
            print("⏭️  Guardado omitido. Puedes ajustar las plantillas y reintentar.")
            return False

    except Exception as e:
        print(f"\n❌ Error de conexión con LM Studio: {e}")
        print(
            "Asegúrate de que LM Studio está abierto, el servidor local iniciado "
            "en el puerto 1234 y la opción CORS activada."
        )
        return False


def modo_automatico() -> None:
    """Ejecuta los 7 pasos en secuencia sin confirmaciones interactivas."""
    print("\n🤖 MODO AUTOMÁTICO — ejecutando los 7 pasos en secuencia\n")
    for paso in sorted(FLUJO.keys()):
        exito = ejecutar_paso(paso, auto=True)
        if not exito:
            print(f"\n⛔ Pipeline detenido en el paso {paso} por error de conexión.")
            sys.exit(1)
    print("\n🏁 Pipeline completo. Todos los archivos han sido generados.")


def mostrar_ayuda() -> None:
    print("""
Uso:
  python orquestador.py <paso>        Ejecuta un paso concreto (1-7)
  python orquestador.py --auto        Ejecuta los 7 pasos en secuencia sin confirmaciones
  python orquestador.py --status      Muestra qué archivos de output existen ya

Pasos disponibles:
  1 — Planificación y Arquitectura
  2 — Generación de Código
  3 — Debugging (Detective)
  4 — Code Review (Crítico)
  5 — Refactoring (Optimizador)
  6 — Testing (Escudo)
  7 — Documentación (Narrador)

Flujo de encadenamiento:
  idea_inicial → [1] → arquitectura → [2] → código → [3] → código corregido
  → [4] reporte revisión
  → [5] → código refactorizado → [6] → tests
                               → [7] → README
""")


def mostrar_status() -> None:
    """Muestra qué archivos de output ya existen."""
    print("\n📊 Estado del pipeline:\n")
    for paso, config in FLUJO.items():
        output = config["output"]
        existe = "✅" if os.path.exists(output) else "⬜"
        print(f"  {existe}  Paso {paso} — {config['nombre']}")
        print(f"         {output}")
    print()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        mostrar_ayuda()
        sys.exit(0)

    arg = sys.argv[1]

    if arg == "--auto":
        modo_automatico()
    elif arg == "--status":
        mostrar_status()
    elif arg == "--help" or arg == "-h":
        mostrar_ayuda()
    else:
        ejecutar_paso(arg)
