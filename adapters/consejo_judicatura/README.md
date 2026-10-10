# Consejo de la Judicatura — candidato Python independiente

Estado: `NOT_APPROVED`; versión candidata `0.1.0-candidate`; portal técnico 6; documentos 73–76. Deriva del handler histórico `judicatura_v1.py` (commit `627842b77dd582798917a410c929d96c635e8540`, rama `codex/judicatura-handler-v1`) y del candidato mantenido en el PR RPA #11.

`adapter.py` implementa `DOCUMENT_FUNCTIONS`; `app.py --context <JSON-privado>` ejecuta documentos por identificación/nombre con Playwright, conserva la página durante el lote y guarda PNG íntegro fuera del repositorio. Un reCAPTCHA visible produce `HUMAN_REQUIRED` y bloquea búsquedas posteriores en la misma sesión; no se resuelve ni evade. Timeout o postcondición no verificada queda `RETRYABLE`, nunca `NO_MATCH`.

No se ha completado aquí una corrida real standalone por documento ni existe elegibilidad vigente para estos documentos en el snapshot TEST del checkpoint. La rama no tiene Release ni firma de módulo; no consumir desde el robot hasta aprobar la cobertura por documento.

Las pruebas sintéticas verifican los cuatro handlers, clasificación positiva/negativa, barrera humana y timeout; no consultan portales ni ORDS. En el RPA fuente, `adapters/supercias/tests` y `adapters/consejo_judicatura/tests` obtuvieron juntas 17 pruebas PASS. Esta evidencia no sustituye exploración real ni certificación.
