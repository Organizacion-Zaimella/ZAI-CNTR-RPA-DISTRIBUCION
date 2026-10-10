# IESS — candidato Python independiente

Estado: `NOT_APPROVED`; versión candidata `0.1.3-candidate`; portal técnico 2; documento 2. La aplicación standalone obtuvo previamente un PDF nativo válido en TEST. Este candidato corrige la interfaz dinámica del sidecar para usar el mismo textbox único sin filtro de nombre accesible y valida `%PDF-`, `startxref`, `%%EOF` y tamaño antes de entregar evidencia.

`app.py --context <JSON-privado>` es la aplicación independiente; `src/adapter.py` exporta `DOCUMENT_FUNCTIONS` para el motor. El sidecar usa el evento de descarga nativo mediante la fachada estable del motor, siguiendo la adquisición PDF de los workflows IESS históricos (`pdf.acquire`). No repite el clic como fallback especulativo. El contexto y las evidencias deben permanecer fuera del repositorio. CAPTCHA/ALTCHA devuelve `HUMAN_REQUIRED`; timeout/error se clasifica como `RETRYABLE`, nunca como ausencia concluyente.

El cambio dinámico está probado con navegador/ORDS sintéticos (5 casos) además del contrato previo. Aún no se ha repetido la corrida integrada usando este candidato; la asignación vigente de ORDS sigue en `iess@0.1.0-candidate`. No existe release firmado para la versión 0.1.3. La correspondencia del evento download con el IESS actual requiere una prueba integrada prudente; no se infiere del resultado histórico por sí solo.
