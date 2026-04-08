Implementa el proyecto COMPLETO según la arquitectura definida en el INPUT. Este es el paso más importante del pipeline: el código que entregues debe poder ejecutarse sin modificaciones.

## Fase 0 — Pre-generación (obligatoria, antes de escribir código)

Antes de generar ningún archivo, lee en este orden:

1. `convenciones_proyecto.md` — fuente de verdad para este proyecto
2. `arquitectura.md` — diseño técnico aprobado

Luego completa este análisis en tu respuesta:

**0.1 — Inventario de archivos**
Lista todos los archivos que vas a generar, en el orden exacto en que los entregarás.

**0.2 — Mapa de dependencias críticas**
Responde estas preguntas sobre el proyecto concreto:

- ¿El proyecto define un modelo de usuario custom? → Si sí, configuración explícita obligatoria.
- ¿Qué modelos existen y en qué módulo vive cada uno? → Ningún modelo en el archivo raíz.
- ¿El proyecto usa operaciones concurrentes? → Si sí, identificar cuáles necesitan bloqueo + transacción.
- ¿El proyecto usa tareas asíncronas? → Sí o no, según `convenciones_proyecto.md`. Si no, no generar archivos de tasks ni configuración de broker.
- ¿Qué módulos tienen modelos? → Todos deben estar registrados en la configuración principal.

**0.3 — Tabla de símbolos por archivo**
Para los archivos más complejos, lista los símbolos externos que usarás y de dónde los importarás. Solo incluye los archivos que realmente existen en este proyecto.

```
controlador_principal.[ext]:
  - [Símbolo] → [from módulo import Símbolo]
  - [etc.]

servicio_principal.[ext]:
  - [lista de símbolos y su origen]
```

Esta tabla es tu contrato. Cuando generes cada archivo, copia los imports de aquí.

---

## Reglas absolutas

**REGLA 1 — COMPLETITUD:** Genera TODOS los archivos listados en la arquitectura. Prohibido escribir "el resto de la implementación es similar", "aquí iría el código de X", o "implementación omitida por brevedad".

**REGLA 2 — FORMATO DE ARCHIVO:** Cada archivo va precedido de su ruta completa:

```[lenguaje] filename: ruta/completa/del/archivo.[ext]

**REGLA 3 — ORDEN DE ENTREGA:**
1. Archivo de dependencias
2. Variables de entorno de ejemplo
3. Configuración principal
4. Modelos — empezando por los que no tienen dependencias
5. Capa de servicios
6. Controladores / vistas
7. Rutas / URLs
8. Tareas asíncronas (solo si el proyecto las usa)
9. Tests y fixtures

**REGLA 4 — CALIDAD:** Aplica todas las convenciones de `convenciones_proyecto.md`. Tipado estático en funciones y métodos públicos. Manejo explícito de errores. Lógica de negocio solo en servicios.

**REGLA 5 — IMPORTS:** Cada archivo importa todo lo que usa. Usa la tabla del Paso 0.3 como referencia. Cada archivo es una isla — no mires otros archivos para asumir qué está disponible.

**REGLA 6 — DEPENDENCIAS:** Versiones fijadas para todas las dependencias directas.

**REGLA 7 — UN MODELO, UN ARCHIVO:** Cada modelo en el archivo de su módulo. El archivo raíz de modelos se entrega VACÍO.

**REGLA 8 — MODELO DE USUARIO CUSTOM:** Si hay usuario custom, la configuración principal lo registra. Todas las relaciones al usuario usan la referencia indirecta configurada, nunca la clase importada directamente.

**REGLA 9 — TAREAS ASÍNCRONAS (condicional):** Solo aplica si `convenciones_proyecto.md` indica que el proyecto usa tasks.
- Las operaciones I/O pesadas van en tasks, nunca en servicios directamente.
- Las tasks definen número máximo de reintentos y delay entre intentos.
- El modo síncrono/eager NUNCA va en la configuración principal. Solo en el entorno de tests como fixture.
- Si el proyecto NO usa tasks: no generes archivos de tasks ni configuración de broker.

**REGLA 10 — OPERACIONES CONCURRENTES:** Cualquier operación de bloqueo DEBE estar dentro de una transacción explícita.

**REGLA 11 — CAMPOS CON VALORES ACOTADOS:** El tamaño máximo cubre el valor almacenado más largo, no el label visible. Usa el mecanismo de enums del framework.

**REGLA 12 — SIN DUPLICADOS:** Cada modelo y cada función de task existe en un único archivo.

## Al final de todos los archivos

Incluye la Tabla de Verificación de Integridad del Constructor con todos los checks completados.

Luego la sección "Cómo ejecutar el proyecto" con comandos exactos:
1. Instalar dependencias
2. Configurar variables de entorno
3. Inicializar base de datos
4. Levantar servicios auxiliares (solo si el proyecto los usa)
5. Levantar el servidor
6. Verificar que funciona
```
