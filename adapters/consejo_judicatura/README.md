# Consejo de la Judicatura — candidato Python independiente

Estado: `NOT_APPROVED`; versión candidata `0.1.0-candidate`; portal técnico 6; documentos 73–76. Deriva del handler histórico `judicatura_v1.py` (commit `627842b77dd582798917a410c929d96c635e8540`, rama `codex/judicatura-handler-v1`) y del candidato mantenido en el PR RPA #11.

`adapter.py` implementa `DOCUMENT_FUNCTIONS`; `app.py --context <JSON-privado>` ejecuta documentos por identificación/nombre con Playwright, conserva la página durante el lote y guarda PNG íntegro fuera del repositorio. Un reCAPTCHA visible produce `HUMAN_REQUIRED` y bloquea búsquedas posteriores en la misma sesión; no se resuelve ni evade. Timeout o postcondición no verificada queda `RETRYABLE`, nunca `NO_MATCH`.

No se ha completado aquí una corrida real standalone por documento ni existe elegibilidad vigente para estos documentos en el snapshot TEST del checkpoint. La rama no tiene Release ni firma de módulo; no consumir desde el robot hasta aprobar la cobertura por documento.

Las pruebas sintéticas verifican los cuatro handlers, clasificación positiva/negativa, barrera humana y timeout; no consultan portales ni ORDS. En el RPA fuente, `adapters/supercias/tests` y `adapters/consejo_judicatura/tests` obtuvieron juntas 17 pruebas PASS. Esta evidencia no sustituye exploración real ni certificación.

## Exploración visible — 2026-10-10

En una sesión de navegador persistente se abrió una vez la ruta de documento
usada por el candidato. La página de Consulta de Procesos mostró los cuatro
campos esperados (actor por identificación/nombre y demandado por
identificación/nombre), el botón BUSCAR y la tabla de resultados. El DOM tenía
dos iframes de reCAPTCHA, ambos ocultos en ese estado inicial. No se ingresó
identificación o nombre, no se pulsó BUSCAR y no se verificó cómo se comporta
el portal después de consultar. La observación confirma solo la carga inicial
de la pantalla; la pareja actual no es elegible en el plan TEST y la URL aún
debe cotejarse con la URL de paso 1 que entregue ORDS cuando haya una pareja
ejecutable.
