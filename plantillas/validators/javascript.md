# Reglas de validación — JavaScript / Node.js

Revisa el código JavaScript/TypeScript generado y corrige todos los errores según estas reglas.

## Errores críticos a detectar y corregir

### 1. `require` y `import` mezclados en el mismo archivo
**Detectar:** un archivo que usa tanto `require()` (CommonJS) como `import` (ESM).
**Corrección:** elige un sistema y aplícalo consistentemente en todo el archivo. Si el proyecto usa ESM (`"type": "module"` en package.json), usa `import`. Si usa CommonJS, usa `require`.

### 2. Promesas sin manejo de error
**Detectar:** llamadas `.then()` sin `.catch()`, o `async/await` sin `try/catch`.
**Corrección:**
```javascript
// Mal
const data = await fetchData();

// Bien
try {
    const data = await fetchData();
} catch (error) {
    console.error('Error:', error);
    throw error;
}
```

### 3. Variables declaradas con `var`
**Detectar:** cualquier uso de `var`.
**Corrección:** reemplaza por `const` (si no se reasigna) o `let` (si se reasigna).

### 4. Credenciales hardcodeadas
**Detectar:** strings literales asignados a variables con nombre `password`, `secret`, `apiKey`, `token`, `key`.
**Corrección:**
```javascript
// Mal
const apiKey = "sk-1234abcd";

// Bien
const apiKey = process.env.API_KEY;
```

### 5. Callback hell sin async/await
**Detectar:** más de 2 niveles de callbacks anidados.
**Corrección:** refactoriza usando `async/await`.

### 6. `console.log` en código de producción
**Detectar:** `console.log` fuera de archivos de test.
**Corrección:** reemplaza por un logger apropiado (`winston`, `pino`, etc.) o elimina.

### 7. Módulos importados pero no usados
**Detectar:** imports o requires cuyo símbolo no aparece en el resto del archivo.
**Corrección:** elimina el import no usado.

## Formato de entrega

Entrega únicamente los archivos que contienen errores, completos y corregidos:
```javascript filename: ruta/completa/del/archivo.js

Al final del output añade una tabla de confirmación:
| Archivo | Error corregido |
|---------|----------------|
| ruta/archivo.js | descripción del fix |
