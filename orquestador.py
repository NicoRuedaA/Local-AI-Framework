"""
orquestador.py — Local AI Framework (v2.1)

MEJORAS IMPLEMENTADAS:
  1. Crítico (paso 4) alimenta al Optimizador (paso 5) — retroalimentación real entre agentes.
  2. Memoria acumulativa entre proyectos — context.md persiste el historial de decisiones.
  3. Soporte multi-modelo y multi-proveedor — LM Studio (local) + Gemini (Google AI Studio).
  4. Soporte multi-archivo — extrae bloques de código y los guarda como archivos individuales.
  5. Manejo de errores con reintentos — reintentos automáticos y detección de outputs vacíos.

PROVEEDORES SOPORTADOS:
  - lmstudio  → modelos locales vía LM Studio (puerto 1234)
  - gemini    → Google Gemini vía API key de Google AI Studio

CONFIGURACIÓN (modelos.json):
  {
    "arquitecto":  {"proveedor": "gemini",   "modelo": "gemini-2.0-flash"},
    "constructor": {"proveedor": "lmstudio", "modelo": "qwen2.5-coder-32b"},
    ...
  }
"""

import os
import sys
import json
import re
import time
from datetime import datetime
from openai import OpenAI

# ──────────────────────────────────────────────
# PROVEEDORES
# ──────────────────────────────────────────────

# Nombres exactos de tus modelos en LM Studio (ajusta si difieren)
NOMBRE_QWEN_32B = "qwen2.5-coder-32b-instruct"
NOMBRE_QWEN_7B  = "qwen2.5-coder-7b-instruct"

# Modelo Gemini recomendado con la API gratuita de Google AI Studio
NOMBRE_GEMINI   = "gemini-2.0-flash"

MODELOS_DEFAULT = {
    "arquitecto":  {"proveedor": "gemini",   "modelo": NOMBRE_GEMINI},
    "constructor": {"proveedor": "lmstudio", "modelo": NOMBRE_QWEN_32B},
    "detective":   {"proveedor": "lmstudio", "modelo": NOMBRE_QWEN_32B},
    "critico":     {"proveedor": "gemini",   "modelo": NOMBRE_GEMINI},
    "optimizador": {"proveedor": "lmstudio", "modelo": NOMBRE_QWEN_32B},
    "escudo":      {"proveedor": "lmstudio", "modelo": NOMBRE_QWEN_7B},
    "narrador":    {"proveedor": "lmstudio", "modelo": NOMBRE_QWEN_7B},
}

def cargar_modelos() -> dict:
    """
    Carga la configuración de modelos desde modelos.json si existe.
    Formato esperado:
        {
          "arquitecto":  {"proveedor": "gemini",   "modelo": "gemini-2.0-flash"},
          "constructor": {"proveedor": "lmstudio", "modelo": "qwen2.5-coder-32b-instruct"}
        }
    Si el archivo no existe, usa MODELOS_DEFAULT.
    """
    ruta = "modelos.json"
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        # Ignorar claves que empiecen por _ (comentarios)
        datos_limpios = {k: v for k, v in datos.items() if not k.startswith("_")}
        modelos = {**MODELOS_DEFAULT, **datos_limpios}
        print(f"📦 Configuración de modelos cargada desde {ruta}")
        return modelos
    print("📦 Usando configuración de modelos por defecto (Gemini + Qwen local)")
    return MODELOS_DEFAULT.copy()

MODELOS = cargar_modelos()


def _leer_gemini_api_key() -> str:
    """
    Lee la API key de Gemini desde la variable de entorno GEMINI_API_KEY
    o desde el archivo .env en la raíz del proyecto.
    """
    # 1. Variable de entorno
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        return key
    # 2. Archivo .env
    if os.path.exists(".env"):
        with open(".env", "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith("GEMINI_API_KEY="):
                    return linea.split("=", 1)[1].strip()
    return ""


def llamar_gemini(api_key: str, modelo: str, system_prompt: str, user_prompt: str, temperature: float) -> str:
    """
    Llama a la API de Google AI Studio (Gemini) usando el endpoint compatible con OpenAI.
    Gemini expone un endpoint /v1beta/openai/ que acepta el mismo formato que OpenAI.
    """
    cliente = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=api_key,
    )
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=temperature,
    )
    return respuesta.choices[0].message.content


def get_config_agente(agente: str) -> tuple[str, str]:
    """Devuelve (proveedor, nombre_modelo) para el agente dado."""
    config = MODELOS.get(agente, {"proveedor": "lmstudio", "modelo": "local-model"})
    return config["proveedor"], config["modelo"]


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
        # Tras guardar, activa el paso 2.5 si hay validators configurados
        "activar_validacion": True,
    },
    "2.5": {
        "nombre":     "Reparador de Código",
        "agente_key": "constructor",
        "agente":     "plantillas/agents/02_agente_constructor.md",
        "prompt":     "plantillas/prompts/02.5_prompt_reparacion.md",
        "input":      "mi_proyecto_actual/src/02_codigo_generado.md",
        # Las reglas de validación del lenguaje se inyectan desde los .md de validators/
        # El bloque se construye dinámicamente en ejecutar_paso
        "output":     "mi_proyecto_actual/src/02.5_codigo_reparado.md",
        "temperature": 0.1,
        # Solo se ejecuta si validaciones.json tiene validators configurados
        "condicional_validators": True,
    },
    "3": {
        "nombre":  "Debugging (Detective)",
        "agente_key": "detective",
        "agente":  "plantillas/agents/03_agente_detective.md",
        "prompt":  "plantillas/prompts/03_prompt_resolucion.md",
        # Lee el código reparado si existe, si no el generado original
        "input":          "mi_proyecto_actual/src/02.5_codigo_reparado.md",
        "input_fallback": "mi_proyecto_actual/src/02_codigo_generado.md",
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
# VALIDACIÓN BASADA EN AGENTE — plugins .md por lenguaje
# Configuración en validaciones.json — sin código específico de lenguaje
# ──────────────────────────────────────────────

RUTA_ERRORES      = "mi_proyecto_actual/src/02.5_errores_validacion.md"
RUTA_VALIDACIONES = "validaciones.json"

def cargar_validators_md() -> str:
    """
    Lee validaciones.json para saber qué .md de validación cargar,
    y devuelve el contenido concatenado de todos ellos.

    Formato de validaciones.json:
        {
          "validators": [
            "plantillas/validators/python.md",
            "plantillas/validators/django.md"
          ]
        }

    Si el archivo no existe o no hay validators, devuelve cadena vacía
    (el paso 2.5 se omitirá por falta de reglas).
    """
    if not os.path.exists(RUTA_VALIDACIONES):
        return ""

    with open(RUTA_VALIDACIONES, "r", encoding="utf-8") as f:
        datos = json.load(f)

    rutas = [v for k, v in datos.items() if k == "validators"]
    if not rutas or not rutas[0]:
        return ""

    bloques = []
    for ruta in rutas[0]:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                bloques.append(f"### Reglas de: {ruta}\n\n{f.read().strip()}")
        else:
            print(f"   ⚠️  Validator no encontrado: {ruta}")

    return "\n\n".join(bloques)


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
    proveedor: str,
    modelo: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float,
) -> str | None:
    """
    Llama al modelo correcto según el proveedor, con reintentos automáticos.
    Proveedores soportados: 'lmstudio', 'gemini'.
    Devuelve el texto generado o None si todos los intentos fallan.
    """
    gemini_key = _leer_gemini_api_key() if proveedor == "gemini" else ""

    if proveedor == "gemini" and not gemini_key:
        print("\n❌ Proveedor 'gemini' configurado pero no se encontró GEMINI_API_KEY.")
        print("   Añádela como variable de entorno o en un archivo .env en la raíz:")
        print("   GEMINI_API_KEY=tu_clave_aqui")
        return None

    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            if proveedor == "gemini":
                resultado = llamar_gemini(gemini_key, modelo, system_prompt, user_prompt, temperature)
            else:
                # lmstudio u otro proveedor compatible con OpenAI
                cliente = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
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
                raise ValueError(f"Output sospechosamente corto ({len(resultado.strip())} chars).")

            return resultado

        except Exception as e:
            print(f"\n⚠️  Intento {intento}/{MAX_REINTENTOS} fallido [{proveedor}/{modelo}]: {e}")
            if intento < MAX_REINTENTOS:
                print(f"   ⏳ Reintentando en {PAUSA_ENTRE_REINTENTOS}s...")
                time.sleep(PAUSA_ENTRE_REINTENTOS)
            else:
                print("\n❌ Todos los reintentos agotados.")
                if proveedor == "lmstudio":
                    print("   Verifica que LM Studio está abierto, servidor en puerto 1234 y CORS activado.")
                elif proveedor == "gemini":
                    print("   Verifica tu GEMINI_API_KEY y que tienes cuota disponible en Google AI Studio.")
                return None


# ──────────────────────────────────────────────
# PROGRESO DEL PIPELINE
# ──────────────────────────────────────────────

def _barra_progreso(completados: int, total: int, tiempos: list[float]) -> None:
    """
    Imprime barra de progreso con %, pasos completados, tiempo transcurrido y ETA.
    """
    pct     = int((completados / total) * 100)
    relleno = int(pct / 5)
    barra   = "█" * relleno + "░" * (20 - relleno)

    if tiempos:
        media        = sum(tiempos) / len(tiempos)
        eta_seg      = int(media * (total - completados))
        eta_m, eta_s = divmod(eta_seg, 60)
        trans_m, trans_s = divmod(int(sum(tiempos)), 60)
        eta_txt   = f"{eta_m}m {eta_s:02d}s"
        trans_txt = f"{trans_m}m {trans_s:02d}s"
    else:
        eta_txt = trans_txt = "--"

    print(f"\n  [{barra}] {pct}%  —  {completados}/{total} pasos completados")
    print(f"  ⏱  Transcurrido: {trans_txt}   |   ETA restante: {eta_txt}\n")


# ──────────────────────────────────────────────
# EJECUCIÓN DE UN PASO
# ──────────────────────────────────────────────

def ejecutar_paso(paso: str, auto: bool = False,
                  completados: int = 0, tiempos: list[float] | None = None) -> bool:
    """
    Ejecuta un paso del flujo. Devuelve True si se guardó el resultado, False si falló o se canceló.
    completados y tiempos se usan para mostrar el progreso en modo automático.
    """
    if paso not in FLUJO:
        print(f"❌ Error: El paso '{paso}' no existe. Usa un número del 1 al 7.")
        return False

    config = FLUJO[paso]
    agente_key = config["agente_key"]
    proveedor, modelo = get_config_agente(agente_key)

    total_pasos = len(FLUJO)

    # ── Paso condicional: solo ejecutar si hay validators configurados ──
    if config.get("condicional_validators"):
        validators_md = cargar_validators_md()
        if not validators_md:
            print(f"\n⏭️  Paso {paso} omitido — no hay validators configurados en validaciones.json.")
            return True

    # Mostrar progreso si estamos en modo automático
    if auto and tiempos is not None:
        _barra_progreso(completados, total_pasos, tiempos)

    print(f"\n{'='*55}")
    print(f"🚀 Paso {paso}/{total_pasos} — {config['nombre']}  [{proveedor} / {modelo}]")
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

    # input con fallback: usa el principal si existe, si no el fallback
    ruta_input = config["input"]
    if "input_fallback" in config and not os.path.exists(ruta_input):
        ruta_input = config["input_fallback"]
        print(f"  ⚠️  Input principal no encontrado, usando fallback: {ruta_input}")

    contenido_input = leer_archivo(ruta_input)

    # Bloque extra: reporte del Crítico (paso 5) o reglas de validators (paso 2.5)
    bloque_extra = ""
    if "input_extra" in config:
        extra = leer_archivo(config["input_extra"])
        tag   = config.get("input_extra_tag", "REPORTE DE REVISIÓN DEL CRÍTICO")
        bloque_extra = f"\n=== {tag} ===\n{extra}\n"

    # Paso 2.5: inyectar las reglas de validación desde los .md de validators/
    if config.get("condicional_validators"):
        validators_md = cargar_validators_md()
        bloque_extra += f"\n=== REGLAS DE VALIDACIÓN DEL LENGUAJE ===\n{validators_md}\n"

    user_prompt = f"""=== ESTADO ACTUAL DEL PROYECTO (INPUT) ===
{contenido_input}
{bloque_extra}
=== TU TAREA ACTUAL ===
{leer_archivo(config['prompt'])}
"""

    print("\n🧠 Consultando modelo... (puede tardar unos segundos)\n")
    t_inicio = time.time()

    resultado = llamar_modelo(proveedor, modelo, system_prompt, user_prompt, config["temperature"])
    t_paso = time.time() - t_inicio
    if resultado is None:
        return False

    print(f"  ⏱  Tiempo del modelo: {int(t_paso // 60)}m {int(t_paso % 60):02d}s")

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

    # Registrar tiempo de este paso para el cálculo de ETA
    if tiempos is not None:
        tiempos.append(t_paso)

    print(f"🎉 Paso {paso} completado{'  (modo automático)' if auto else ''}.  [{int(t_paso // 60)}m {int(t_paso % 60):02d}s]")
    return True


# ──────────────────────────────────────────────
# MODOS DE EJECUCIÓN
# ──────────────────────────────────────────────

def modo_automatico() -> None:
    """Ejecuta todos los pasos en secuencia sin confirmaciones interactivas."""
    print("\n🤖 MODO AUTOMÁTICO — ejecutando el pipeline completo\n")
    tiempos: list[float] = []

    # Orden explícito para garantizar que 2.5 va entre 2 y 3
    pasos = ["1", "2", "2.5", "3", "4", "5", "6", "7"]
    total = len(pasos)

    for i, paso in enumerate(pasos):
        exito = ejecutar_paso(paso, auto=True, completados=i, tiempos=tiempos)
        if not exito:
            print(f"\n⛔ Pipeline detenido en el paso {paso} por error irrecuperable.")
            sys.exit(1)

    # Barra al 100% al terminar
    _barra_progreso(total, total, tiempos)

    total_seg        = int(sum(tiempos))
    total_m, total_s = divmod(total_seg, 60)
    print(f"🏁 Pipeline completo en {total_m}m {total_s:02d}s. Todos los archivos generados.")

    print("\n💤 Apagando el equipo en 60 segundos...")
    os.system("shutdown /s /t 60")


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
    """Muestra qué archivos de output ya existen, con porcentaje de progreso."""
    pasos      = list(FLUJO.items())
    total      = len(pasos)
    completados = sum(1 for _, c in pasos if os.path.exists(c["output"]))
    pct        = int((completados / total) * 100)
    relleno    = int(pct / 5)
    barra      = "█" * relleno + "░" * (20 - relleno)

    print(f"\n📊 Estado del pipeline:\n")
    print(f"  [{barra}] {pct}%  —  {completados}/{total} pasos completados\n")

    for paso, config in pasos:
        output = config["output"]
        if os.path.exists(output):
            tam = os.path.getsize(output)
            print(f"  ✅ Paso {paso} — {config['nombre']}  ({tam:,} bytes)")
        else:
            print(f"  ⬜ Paso {paso} — {config['nombre']}  (pendiente)")
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
