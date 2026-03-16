import os

# 1. Definimos las carpetas de nuestra arquitectura
carpetas = [
    "plantillas/agents",
    "plantillas/prompts",
    "plantillas/skills",
    "mi_proyecto_actual/01_spec",
    "mi_proyecto_actual/src"
]

# 2. Definimos los archivos clave que deben existir (con un texto de ayuda)
archivos = {
    "index.md": """# Contexto Global del Entorno de Desarrollo Automático

Estás operando como el cerebro de una agencia de desarrollo de software automatizada. Este entorno está dividido en dos grandes bloques:

## 1. /plantillas (Tu Motor Lógico - NO MODIFICAR)
Esta carpeta contiene tu configuración base.
- `/plantillas/agents/`: Define la personalidad.
- `/plantillas/prompts/`: Contiene la tarea.
- `/plantillas/skills/`: Contiene el conocimiento técnico base.

## 2. /mi_proyecto_actual (Tu Espacio de Trabajo - AQUÍ TRABAJAS)
Esta es la carpeta específica del proyecto que estamos construyendo.
- `/01_spec/`: Contiene los documentos de arquitectura y la idea.
- `/src/`: Aquí debes volcar el código fuente que generes.
""",
    "plantillas/skills/convenciones.md": """# Convenciones Técnicas Obligatorias
- Escribe el código de forma modular y limpia (Clean Code).
- Añade comentarios solo en lógica compleja.
- Utiliza nombres de variables descriptivos en inglés o español, pero mantén la coherencia.
""",
    "mi_proyecto_actual/01_spec/idea_inicial.md": """## Proyecto
[ESCRIBE AQUÍ TU IDEA. Ej: Una API REST para gestionar tareas de un equipo]

## Requisitos clave
- [Requisito 1]
- [Requisito 2]
- Restricciones técnicas: [Ej: Usar Python con FastAPI y SQLite]
"""
}

def construir_entorno():
    print("🏗️ Construyendo tu entorno de IA autónoma...\n")
    
    # Crear los directorios
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)
        print(f"📁 Creado directorio: {carpeta}/")
        
    # Crear los archivos base
    for ruta_archivo, contenido_base in archivos.items():
        if not os.path.exists(ruta_archivo):
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(contenido_base)
            print(f"📄 Creado archivo base: {ruta_archivo}")
        else:
            print(f"⚠️ Omitido: {ruta_archivo} (Ya existe)")
            
    print("\n✅ ¡Entorno base creado con éxito!")
    print("👉 Siguiente paso: Mueve los 14 archivos de Prompts y Agentes a sus carpetas correspondientes en /plantillas.")

if __name__ == "__main__":
    construir_entorno()