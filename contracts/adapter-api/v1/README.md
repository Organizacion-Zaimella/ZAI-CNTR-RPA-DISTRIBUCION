# Contrato de adaptadores — propuesta v1

**Precedencia C.145:** esta página es una propuesta histórica y no define por sí sola el ABI ejecutable. Para la integración vigente se usa el ABI del motor/sidecar en la rama candidata RPA, documentado en [README/contratos RPA](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/tree/codex/cntr-rpa-1.0.0-c145). El sidecar resuelve la función por documento expuesta en DOCUMENT_FUNCTIONS; no ejecutar workflows ni importar OpenClaw.

Cada adaptador futuro corresponderá a un portal confirmado en Oracle, con funciones por `document_id`, versión propia y rango de compatibilidad con el motor. El motor entregará por un canal IPC acotado los parámetros autorizados por ORDS y servicios de navegador/evidencia; el adaptador no recibirá OAuth ORDS ni decidirá el siguiente trabajo.

Operaciones conceptuales: `prepare(context)`, `execute_document(context, services)`, `resume(checkpoint)` y `close()`. Resultado tipado: `MATCH`, `NO_MATCH`, `HUMAN_REQUIRED`, `RETRYABLE` o `ERROR`. `NO_MATCH` exige evidencia verificable de ausencia. La propiedad de Playwright Page/context, los tipos exactos, plazos y limpieza se cerrarán antes de implementar.

Esta carpeta es documentación de diseño. No sustituye la interfaz implementada en el RPA, no se importa desde el motor y no certifica adaptadores.
