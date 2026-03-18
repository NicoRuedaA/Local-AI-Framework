"""
orquestador.py — Local AI Framework (v2)

MEJORAS IMPLEMENTADAS:
  1. Crítico (paso 4) alimenta al Optimizador (paso 5) — retroalimentación real entre agentes.
  2. Memoria acumulativa entre proyectos — context.md persiste el historial de decisiones.
  3. Soporte multi-modelo — cada agente puede usar un modelo distinto vía modelos.json.
  4. Soporte multi-archivo — extrae bloques de código y los guarda como archivos individuales.
  5. Manejo de errores con reintentos — reintentos automáticos y detección de outputs vacíos.
"""

import os
import sys
import json
import re
import time
from datetime import datetime
from openai import OpenAI

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE MODELOS (MEJORA 3)
# ──────────────────────────────────────────────

MODELOS_DEFAULT = {
    "arquitecto":  "local-model",
    "constructor": "local-model",
    "detective":   "local-model",
    "critico":     "local-model",
    "optimizador": "local-model",
    "escudo":      "local-model",
    "narrador":    "local-model",
}

def cargar_modelos() -> dict:
    """
    Carga la configuración de modelos desde modelos.json si existe.
    Permite asignar un modelo distinto a cada agente:

        {
          "arquitecto":  "deepseek-coder-33b",
          "constructor": "qwen2.5-coder-7b",
          ...
        }

    Si el archivo no existe, usa el modelo por defecto para todos.
    """
    ruta = "modelos.json"
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        modelos = {**MODELOS_DEFAULT, **datos}
        print(f"📦 Configuración de modelos cargada desde {ruta}")
        return modelos
    return MODELOS_DEFAULT.copy()

MODELOS = cargar_modelos()

def get_cliente(agente: str) -> tuple[OpenAI, str]:
    """Devuelve el cliente OpenAI y el nombre del modelo para el agente dado."""
    modelo = MODELOS.get(agente, "local-model")
    cliente = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    return cliente, modelo


# ──────────────────────────────────────────────
# DEFINICIÓN DEL FLUJO
# MEJORA 1: paso 5 ahora usa TAMBIÉN el reporte del paso 4 como input adicional
# ──────────────────────────────────────────────

FLUJO = {
    "1": {
        "nombre":  "Planificación y Arquitectura",
        "agente_key": "arquitecto",
        "agente":  "plantillas/agents/01_agente_arquitecto.md",
        "prompt":  "plantillas/prompts/01_prompt_planificacion.md",
        "input":   "mi_proyecto_actual/01_spec/idea_inicial.md",
        "output":  "mi_proyecto_actual/01_spec/01_arquitectura.md",
        "temperature": 0.3,
    },
    "2": {
        "nombre":  "Generación de Código",
        "agente_key": "constructor",
        "agente":  "plantillas/agents/02_agente_constructor.md",
        "prompt":  "plantillas/prompts/02_prompt_generacion.md",
        "input":   "mi_proyecto_actual/01_spec/01_arquitectura.md",
        "output":  "mi_proyecto_actual/src/02_codigo_generado.md",
        "temperature": 0.2,
    },
    "3": {
        "nombre":  "Debugging (Detective)",
        "agente_key": "detective",
        "agente":  "plantillas/agents/03_agente_detective.md",
        "prompt":  "plantillas/prompts/03_prompt_resolucion.md",
        "input":   "mi_proyecto_actual/src/02_codigo_generado.md",
        "output":  "mi_proyecto_actual/src/03_codigo_corregido.md",
        "temperature": 0.1,
    },
    "4": {
        "nombre":  "Code Review (Crítico)",
        "agente_key": "critico",
        "agente":  "plantillas/agents/04_agente_critico.md",
        "prompt":  "plantillas/prompts/04_prompt_revision.md",
        "input":   "mi_proyecto_actual/src/03_codigo_corregido.md",
        "output":  "mi_proyecto_actual/src/04_reporte_revision.md",
        "temperature": 0.2,
    },
    "5": {
        "nombre":  "Refactoring (Optimizador)",
        "agente_key": "optimizador",
        "agente":  "plantillas/agents/05_agente_optimizador.md",
        "prompt":  "plantillas/prompts/05_prompt_rendimiento.md",
        "input":   "mi_proyecto_actual/src/03_codigo_corregido.md",
        # MEJORA 1: input_extra hace que el Optimizador reciba también el reporte del Crítico
        "input_extra": "mi_proyecto_actual/src/04_reporte_revision.md",
        "output":  "mi_proyecto_actual/src/05_codigo_refactorizado.md",
        "temperature": 0.2,
    },
    "6": {
        "nombre":  "Testing (Escudo)",
        "agente_key": "escudo",
        "agente":  "plantillas/agents/06_agente_escudo.md",
        "prompt":  "plantillas/prompts/06_prompt_cobertura.md",
        "input":   "mi_proyecto_actual/src/05_codigo_refactorizado.md",
        "output":  "mi_proyecto_actual/src/06_tests.md",
        "temperature": 0.2,
    },
    "7": {
        "nombre":  "Documentación (Narrador)",
        "agente_key": "narrador",
        "agente":  "plantillas/agents/07_agente_narrador.md",
        "prompt":  "plantillas/prompts/07_prompt_tecnica.md",
        "input":   "mi_proyecto_actual/src/05_codigo_refactorizado.md",
        "output":  "mi_proyecto_actual/src/README.md",
        "temperature": 0.5,
    },
}


# ──────────────────────────────────────────────
# MEMORIA ACUMULATIVA (MEJORA 2)
# ──────────────────────────────────────────────

RUTA_CONTEXTO = "mi_proyecto_actual/context.md"

def leer_contexto_acumulado() -> str:
    """Lee el historial de decisiones del proyecto si existe."""
    if os.path.exists(RUTA_CONTEXTO):
        with open(RUTA_CONTEXTO, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def actualizar_contexto(paso: str, nombre: str, resumen: str) -> None:
    """
    Añade una entrada al context.md del proyecto con la fecha, el paso
    y un resumen del output (primeras 300 palabras).
    Esto persiste el historial entre ejecuciones.
    """
    os.makedirs(os.path.dirname(RUTA_CONTEXTO), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    extracto = " ".join(resumen.split()[:300])
    entrada = f"\n---\n### [{timestamp}] Paso {paso} — {nombre}\n{extracto}\n"

    with open(RUTA_CONTEXTO, "a", encoding="utf-8") as f:
        f.write(entrada)
    print(f"📝 Contexto acumulado actualizado: {RUTA_CONTEXTO}")


# ──────────────────────────────────────────────
# SOPORTE MULTI-ARCHIVO (MEJORA 4)
# ──────────────────────────────────────────────

def extraer_y_guardar_archivos(contenido: str, directorio_destino: str) -> list[str]:
    """
    Busca bloques de código con nombre de archivo en el output de la IA y los guarda
    como archivos individuales en directorio_destino.

    Formato reconocido:
        ```python filename: main.py
        ... código ...
        ```
        o
        # filename: utils.py
        ```python
        ... código ...
        ```

    Devuelve la lista de rutas de archivos creados.
    """
    # Patrón 1: ```lang filename: nombre.ext
    patron1 = re.compile(
        r"```[\w+#-]*\s+filename:\s*(\S+)\n(.*?)```",
        re.DOTALL | re.IGNORECASE,
    )
    # Patrón 2: comentario # filename: nombre.ext seguido de bloque ```
    patron2 = re.compile(
        r"#\s*filename:\s*(\S+)\s*\n```[\w+#-]*\n(.*?)```",
        re.DOTALL | re.IGNORECASE,
    )

    archivos_creados = []
    for patron in (patron1, patron2):
        for match in patron.finditer(contenido):
            nombre_archivo = match.group(1).strip()
            codigo = match.group(2)
            ruta_completa = os.path.join(directorio_destino, nombre_archivo)
            os.makedirs(os.path.dirname(ruta_completa) if os.path.dirname(nombre_archivo) else directorio_destino, exist_ok=True)
            with open(ruta_completa, "w", encoding="utf-8") as f:
                f.write(codigo)
            archivos_creados.append(ruta_completa)
            print(f"   📄 Archivo extraído: {ruta_completa}")

    return archivos_creados


# ──────────────────────────────────────────────
# UTILIDADES DE I/O
# ──────────────────────────────────────────────

def leer_archivo(ruta: str) -> str:
    """Lee un archivo. Si no existe, devuelve un aviso en lugar de romper el script."""
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            return f.read().strip()
    return f"[Aviso: No se encontró información en {ruta}. Revisa la ruta o genera el paso anterior primero.]"

def guardar_archivo(ruta: str, contenido: str) -> None:
    """Guarda el archivo creando directorios intermedios si hacen falta."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"\n✅ Guardado en: {ruta}")


# ──────────────────────────────────────────────
# LLAMADA AL MODELO CON REINTENTOS (MEJORA 5)
# ──────────────────────────────────────────────

MAX_REINTENTOS = 3
PAUSA_ENTRE_REINTENTOS = 5  # segundos

def llamar_modelo(
    cliente: OpenAI,
    modelo: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
) -> str | None:
    """
    Llama al modelo con reintentos automáticos en caso de error de red o
    respuesta vacía. Devuelve el texto generado o None si todos los intentos fallan.
    """
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            respuesta = cliente.chat.completions.create(
                model=modelo,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user",   "content": user_prompt},
                ],
                temperature=temperature,
            )
            resultado = respuesta.choices[0].message.content

            # Detectar output vacío o demasiado corto (señal de fallo silencioso)
            if not resultado or len(resultado.strip()) < 50:
                raise ValueError(f"Output sospechosamente corto ({len(resultado.strip())} chars). Posible fallo del modelo.")

            return resultado

        except Exception as e:
            print(f"\n⚠️  Intento {intento}/{MAX_REINTENTOS} fallido: {e}")
            if intento < MAX_REINTENTOS:
                print(f"   ⏳ Reintentando en {PAUSA_ENTRE_REINTENTOS}s...")
                time.sleep(PAUSA_ENTRE_REINTENTOS)
            else:
                print("\n❌ Todos los reintentos agotados.")
                print(
                    "Asegúrate de que LM Studio está abierto, el servidor local iniciado "
                    "en el puerto 1234 y la opción CORS activada."
                )
                return None


# ──────────────────────────────────────────────
# EJECUCIÓN DE UN PASO
# ──────────────────────────────────────────────

def ejecutar_paso(paso: str, auto: bool = False) -> bool:
    """
    Ejecuta un paso del flujo. Devuelve True si se guardó el resultado, False si falló o se canceló.
    """
    if paso not in FLUJO:
        print(f"❌ Error: El paso '{paso}' no existe. Usa un número del 1 al 7.")
        return False

    config = FLUJO[paso]
    agente_key = config["agente_key"]
    cliente, modelo = get_cliente(agente_key)

    print(f"\n{'='*55}")
    print(f"🚀 Paso {paso}/7 — {config['nombre']}  [modelo: {modelo}]")
    print(f"{'='*55}")
    print(f"  📥 Input : {config['input']}")
    if "input_extra" in config:
        print(f"  📥 Extra : {config['input_extra']}  (retroalimentación del Crítico)")
    print(f"  📤 Output: {config['output']}")

    # ── Construir prompts ──────────────────────────────────
    contexto_global   = leer_archivo("index.md")
    skills            = leer_archivo("plantillas/skills/convenciones.md")
    # MEJORA 2: incluir memoria acumulativa en el contexto del sistema
    memoria           = leer_contexto_acumulado()
    contexto_memoria  = f"\n=== HISTORIAL DE DECISIONES DEL PROYECTO ===\n{memoria}" if memoria else ""

    system_prompt = f"""{contexto_global}
{contexto_memoria}

=== TU ROL PARA ESTA TAREA ===
{leer_archivo(config['agente'])}

=== CONVENCIONES TÉCNICAS (SKILLS) ===
{skills}
"""

    contenido_input = leer_archivo(config["input"])

    # MEJORA 1: si hay input_extra (reporte del Crítico), se añade al user prompt
    bloque_extra = ""
    if "input_extra" in config:
        extra = leer_archivo(config["input_extra"])
        bloque_extra = f"""
=== REPORTE DE REVISIÓN DEL CRÍTICO (ÚSALO PARA GUIAR TU REFACTORING) ===
{extra}
"""

    user_prompt = f"""=== ESTADO ACTUAL DEL PROYECTO (INPUT) ===
{contenido_input}
{bloque_extra}
=== TU TAREA ACTUAL ===
{leer_archivo(config['prompt'])}
"""

    print("\n🧠 Consultando modelo... (puede tardar unos segundos)\n")

    resultado = llamar_modelo(cliente, modelo, system_prompt, user_prompt, config["temperature"])
    if resultado is None:
        return False

    # ── Preview ───────────────────────────────────────────
    print("=" * 55)
    print(f"✨ RESPUESTA — {config['nombre']}")
    print("=" * 55)
    preview = resultado[:800]
    print(preview + ("\n\n... [truncado para previsualización]" if len(resultado) > 800 else ""))
    print("=" * 55)

    # ── Confirmar o guardar automáticamente ───────────────
    if not auto:
        confirmacion = input(f"\n¿Guardar en '{config['output']}'? (s/n): ").strip().lower()
        if confirmacion != "s":
            print("⏭️  Guardado omitido. Puedes ajustar las plantillas y reintentar.")
            return False

    guardar_archivo(config["output"], resultado)

    # MEJORA 4: extraer archivos de código individuales si los hay
    directorio_src = "mi_proyecto_actual/src"
    archivos = extraer_y_guardar_archivos(resultado, directorio_src)
    if archivos:
        print(f"   🗂️  {len(archivos)} archivo(s) de código extraído(s) en {directorio_src}/")

    # MEJORA 2: actualizar memoria acumulativa
    actualizar_contexto(paso, config["nombre"], resultado)

    print(f"🎉 Paso {paso} completado{'  (modo automático)' if auto else ''}.")
    return True


# ──────────────────────────────────────────────
# MODOS DE EJECUCIÓN
# ──────────────────────────────────────────────

def modo_automatico() -> None:
    """Ejecuta los 7 pasos en secuencia sin confirmaciones interactivas."""
    print("\n🤖 MODO AUTOMÁTICO — ejecutando los 7 pasos en secuencia\n")
    for paso in sorted(FLUJO.keys()):
        exito = ejecutar_paso(paso, auto=True)
        if not exito:
            print(f"\n⛔ Pipeline detenido en el paso {paso} por error irrecuperable.")
            sys.exit(1)
    print("\n🏁 Pipeline completo. Todos los archivos han sido generados.")


def mostrar_ayuda() -> None:
    print("""
Uso:
  python orquestador.py <paso>        Ejecuta un paso concreto (1-7)
  python orquestador.py --auto        Ejecuta los 7 pasos sin confirmaciones
  python orquestador.py --status      Muestra qué archivos de output ya existen
  python orquestador.py --context     Muestra el historial de decisiones del proyecto
  python orquestador.py --help        Muestra esta ayuda

Pasos disponibles:
  1 — Planificación y Arquitectura
  2 — Generación de Código
  3 — Debugging (Detective)
  4 — Code Review (Crítico)
  5 — Refactoring (Optimizador)   ← ahora recibe el reporte del Crítico (Paso 4)
  6 — Testing (Escudo)
  7 — Documentación (Narrador)

Flujo de encadenamiento (v2):
  idea_inicial → [1] → arquitectura → [2] → código → [3] → código corregido
    → [4] reporte revisión ──────────────────────────┐
    → [5] código refactorizado (usa código + reporte) ┘
    → [6] → tests
    → [7] → README

Configuración de modelos:
  Crea modelos.json en la raíz para asignar un modelo diferente por agente:
  {
    "arquitecto": "deepseek-coder-33b",
    "constructor": "qwen2.5-coder-7b"
  }

Memoria acumulativa:
  El historial de decisiones se guarda en mi_proyecto_actual/context.md
  y se inyecta automáticamente en el contexto de cada paso.

Extracción multi-archivo:
  Si la IA genera bloques con '```python filename: nombre.py', se guardan
  automáticamente como archivos individuales en mi_proyecto_actual/src/.
""")


def mostrar_status() -> None:
    """Muestra qué archivos de output ya existen y el estado de la memoria."""
    print("\n📊 Estado del pipeline:\n")
    for paso, config in FLUJO.items():
        output = config["output"]
        existe = "✅" if os.path.exists(output) else "⬜"
        print(f"  {existe} Paso {paso} — {config['nombre']}")
        print(f"     {output}")
    print()
    tiene_memoria = os.path.exists(RUTA_CONTEXTO)
    print(f"  {'✅' if tiene_memoria else '⬜'} Memoria acumulativa: {RUTA_CONTEXTO}")
    print()


def mostrar_contexto() -> None:
    """Muestra el historial de decisiones guardado en context.md."""
    memoria = leer_contexto_acumulado()
    if memoria:
        print(f"\n📖 Historial de decisiones ({RUTA_CONTEXTO}):\n")
        print(memoria)
    else:
        print(f"\n⚠️  No hay historial todavía. Ejecuta al menos un paso para generarlo.")


# ──────────────────────────────────────────────
# ENTRYPOINT
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        mostrar_ayuda()
        sys.exit(0)

    arg = sys.argv[1]

    if arg == "--auto":
        modo_automatico()
    elif arg == "--status":
        mostrar_status()
    elif arg == "--context":
        mostrar_contexto()
    elif arg in ("--help", "-h"):
        mostrar_ayuda()
    else:
        ejecutar_paso(arg)