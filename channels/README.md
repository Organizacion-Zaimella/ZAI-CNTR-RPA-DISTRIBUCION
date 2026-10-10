# Canales

`test.json` y `test.json.sig` de esta rama apuntan a la generación 9 del canal TEST: prerelease firmado [`cntr-rpa-1.0.0-test.11`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-1.0.0-test.11), motor `1.0.0-test.5` y adaptadores IESS `0.1.3-candidate`, OFAC `0.1.1-candidate` y SRI `0.1.2-candidate`. Todos siguen como candidatos de QA; la firma asegura origen e integridad, no certificación funcional.

El canal está en una rama de tarea para validar la lectura anónima, descarga del motor/adaptadores y ejecución desde un ejecutable instalado. ORDS mantiene IESS fijado a `0.1.0-candidate`, así que esta versión no se activa en el plan actual. No se modifica `main` ni se publica `production.json`. Cada promoción posterior requiere un PR, revisión, firma y generación superior.
