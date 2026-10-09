# Contrato de adaptadores — propuesta v1

Cada adaptador futuro corresponderá a un portal confirmado en Oracle, con funciones por `document_id`, versión propia y rango de compatibilidad con el motor. El motor entregará por un canal IPC acotado los parámetros autorizados por ORDS y servicios de navegador/evidencia; el adaptador no recibirá OAuth ORDS ni decidirá el siguiente trabajo.

Operaciones conceptuales: `prepare(context)`, `execute_document(context, services)`, `resume(checkpoint)` y `close()`. Resultado tipado: `MATCH`, `NO_MATCH`, `HUMAN_REQUIRED`, `RETRYABLE` o `ERROR`. `NO_MATCH` exige evidencia verificable de ausencia. La propiedad de Playwright Page/context, los tipos exactos, plazos y limpieza se cerrarán antes de implementar.

Este directorio documenta requisitos; **todavía no contiene un esquema final ni adaptadores ejecutables**.
