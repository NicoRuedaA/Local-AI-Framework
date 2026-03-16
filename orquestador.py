# Pega aquí el código del script orquestador en Python
import os
import sys
from openai import OpenAI

# Conexión a tu servidor local (LM Studio)
# Asegúrate de que LM Studio está ejecutando el Local Server en el puerto 1234
cliente = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# Diccionario que mapea los 7 pasos completos
FLUJO = {
    "1": {
        "nombre": "Planificación y Arquitectura",
        "agente": "plantillas/agents/01_agente_arquitecto.md",
        "prompt": "plantillas/prompts/01_prompt_planificacion.md",
        "input": "mi_proyecto_actual/01_spec/idea_inicial.md",
        "output": "mi_proyecto_actual/01_spec/01_arquitectura.md"
    },
    "2": {
        "nombre": "Generación de Código",
        "agente": "plantillas/agents/02_agente_constructor.md",
        "prompt": "plantillas/prompts/02_prompt_generacion.md",
        "input": "mi_proyecto_actual/01_spec/01_arquitectura.md",
        "output": "mi_proyecto_actual/src/02_codigo_generado.md"
    },
    "3": {
        "nombre": "Debugging (Detective)",
        "agente": "plantillas/agents/03_agente_detective.md",
        "prompt": "plantillas/prompts/03_prompt_resolucion.md",
        "input": "mi_proyecto_actual/src/02_codigo_generado.md",
        "output": "mi_proyecto_actual/src/03_codigo_corregido.md"
    },
    "4": {
        "nombre": "Code Review (Crítico)",
        "agente": "plantillas/agents/04_agente_critico.md",
        "prompt": "plantillas/prompts/04_prompt_revision.md",
        "input": "mi_proyecto_actual/src/02_codigo_generado.md",
        "output": "mi_proyecto_actual/src/04_reporte_revision.md"
    },
    "5": {
        "nombre": "Refactoring (Optimizador)",
        "agente": "plantillas/agents/05_agente_optimizador.md",
        "prompt": "plantillas/prompts/05_prompt_rendimiento.md",
        "input": "mi_proyecto_actual/src/02_codigo_generado.md",
        "output": "mi_proyecto_actual/src/05_codigo_refactorizado.md"
    },
    "6": {
        "nombre": "Testing (Escudo)",
        "agente": "plantillas/agents/06_agente_escudo.md",
        "prompt": "plantillas/prompts/06_prompt_cobertura.md",
        "input": "mi_proyecto_actual/src/02_codigo_generado.md",
        "output": "mi_proyecto_actual/src/06_tests.md"
    },
    "7": {
        "nombre": "Documentación (Narrador)",
        "agente": "plantillas/agents/07_agente_narrador.md",
        "prompt": "plantillas/prompts/07_prompt_tecnica.md",
        "input": "mi_proyecto_actual/src/02_codigo_generado.md",
        "output": "mi_proyecto_actual/src/README.md"
    }
}

def leer_archivo(ruta):
    """Lee un archivo. Si no existe, devuelve una advertencia en lugar de romper el script."""
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return f.read().strip()
    return f"[Aviso: No se encontró información en {ruta}. El usuario deberá proporcionarla o revisar la ruta.]"

def guardar_archivo(ruta, contenido):
    """Guarda el archivo en la ruta especificada."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"\n✅ Archivo guardado con éxito en: {ruta}")

def ejecutar_paso(paso):
    if paso not in FLUJO:
        print(f"❌ Error: El paso '{paso}' no existe. Usa un número del 1 al 7.")
        sys.exit(1)

    config = FLUJO[paso]
    print(f"🚀 Ejecutando Paso {paso}: {config['nombre']}...\n")

    # 1. Leer contexto base
    contexto_global = leer_archivo("index.md")
    skills = leer_archivo("plantillas/skills/convenciones.md")

    # 2. Ensamblar System Prompt
    system_prompt = f"""
    {contexto_global}
    
    === TU ROL PARA ESTA TAREA ===
    {leer_archivo(config['agente'])}
    
    === CONVENCIONES TÉCNICAS (SKILLS) ===
    {skills}
    """

    # 3. Ensamblar User Prompt
    user_prompt = f"""
    === ESTADO ACTUAL DEL PROYECTO (INPUT) ===
    {leer_archivo(config['input'])}
    
    === TU TAREA ACTUAL ===
    {leer_archivo(config['prompt'])}
    """

    print("🧠 Consultando a tu modelo local en LM Studio... (esto puede tardar unos segundos)")
    
    try:
        # Llamada a LM Studio
        respuesta = cliente.chat.completions.create(
            model="local-model", # LM Studio ignora esto y usa el que tengas cargado
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Temperatura baja para mantener el rigor técnico
        )
        
        resultado = respuesta.choices[0].message.content

        # Previsualización
        print("\n" + "="*50)
        print(f"✨ RESPUESTA DE LA IA ({config['nombre']}) ✨")
        print("="*50)
        # Mostramos solo los primeros 800 caracteres para no inundar la terminal
        print(resultado[:800] + ("\n\n... [Texto truncado para previsualización]" if len(resultado) > 800 else ""))
        print("="*50)

        # Confirmación de guardado
        confirmacion = input(f"\n¿Deseas guardar este resultado en '{config['output']}'? (s/n): ")
        
        if confirmacion.lower() == 's':
            guardar_archivo(config['output'], resultado)
            print(f"🎉 Paso {paso} completado.")
        else:
            print("❌ Guardado cancelado. Puedes ajustar tus plantillas y volver a intentarlo.")
            
    except Exception as e:
        print(f"\n❌ Error de conexión con LM Studio: {e}")
        print("Asegúrate de que LM Studio está abierto, el servidor local iniciado en el puerto 1234 y la opción CORS activada.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python orquestador.py <numero_de_paso>")
        print("Ejemplo: python orquestador.py 1")
        sys.exit(1)
    
    numero_paso = sys.argv[1]
    ejecutar_paso(numero_paso)