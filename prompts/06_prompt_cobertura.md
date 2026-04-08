Escribe la suite de tests COMPLETA para el proyecto del INPUT. Los tests deben poder ejecutarse desde la raíz del proyecto sin configuración adicional más allá de las variables de entorno.

## Archivos a entregar

Adapta los nombres de archivo al stack del proyecto. Como mínimo entrega:

- Archivo de fixtures globales (conftest, factories, helpers de test)
- Tests de autenticación y autorización
- Tests de las entidades principales (CRUD)
- Tests de las operaciones críticas del dominio (según `idea_inicial.md`)
- Tests de edge cases y errores controlados
- Tests de tareas asíncronas (solo si el proyecto las usa)

## Requisitos por categoría

### Happy path (mínimo 2 tests por endpoint o función principal)

- La operación principal con datos válidos produce el resultado esperado
- La respuesta tiene el formato y código de estado correcto

### Autenticación y autorización (obligatorio para cada acción protegida)

- Usuario anónimo intenta acción protegida → error de autenticación
- Usuario sin permisos intenta acción de admin → error de autorización
- Usuario intenta acceder a recursos de otro usuario → error de autorización

### Concurrencia (crítico para las operaciones concurrentes del proyecto)

- Dos requests simultáneos de la misma operación crítica → solo uno tiene efecto
- El sistema mantiene consistencia bajo carga concurrente

### Edge cases

- Campos obligatorios vacíos → error descriptivo
- Recursos que no existen → error apropiado
- Inputs con caracteres especiales o inyecciones → manejo seguro

### Errores controlados

- El sistema falla de forma predecible con el código de error correcto
- Los errores tienen mensajes descriptivos, no trazas de stack

### Integraciones (solo si el proyecto las usa)

- Las tasks asíncronas se encolan exactamente una vez al dispararse la condición
- La task produce el efecto esperado (email, webhook, etc.)
- Si no hay destinatarios, no se produce ningún efecto secundario

## Estándares de calidad

- Nombre de test descriptivo del escenario completo
- Usa el mecanismo de parametrización del framework para variantes del mismo test
- Cada test es independiente: no depende del estado de otro test
- Usa factories para crear objetos de test, no el ORM directamente
- Al final incluye el comando exacto para ejecutar los tests con reporte de cobertura
