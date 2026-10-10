# Superintendencia — candidato Python independiente

Estado: `NOT_APPROVED`; versión candidata `0.1.0-candidate`; portal técnico 1; documentos 13–19. Este código deriva del handler histórico `supercias_v1.py` (commit `24919990e576f81e9171d56e5f0f0a5c09cc792f`, rama `codex/p1-supercias-v39`) y del candidato mantenido en el PR RPA #11.

`adapter.py` implementa `DOCUMENT_FUNCTIONS`; `app.py --context <JSON-privado>` ejecuta el lote independiente con Playwright y mantiene su sesión. El contexto y los PDF de evidencia deben estar fuera del repositorio. El adaptador valida el portal, la identidad de empresa y cada postcondición. Un ALTCHA visible produce `HUMAN_REQUIRED`; error, timeout, evidencia ambigua o PDF inválido no se convierten en `NO_MATCH`.

No se ha probado aquí una corrida real standalone de todos los documentos ni existe elegibilidad vigente para estos documentos en el snapshot TEST del checkpoint. La rama no tiene Release ni firma de módulo; no consumir desde el robot hasta aprobar la cobertura por documento.

Las pruebas de contrato son sintéticas y no consultan portales ni ORDS. En el RPA fuente, `adapters/supercias/tests` obtuvo 17 pruebas PASS junto con Judicatura; esta evidencia no sustituye exploración real ni certificación.
