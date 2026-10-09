# Canales

`test.json` y `test.json.sig` apuntan a la generación 2 del canal TEST: prerelease firmado `cntr-rpa-1.0.0-test.2`, motor CLI 1.0.0 y cinco adaptadores `0.1.0-candidate` (IESS, SRI, OFAC, SERCOP e INTERPOL). Todos están marcados como candidatos de QA; la firma asegura origen e integridad, no resultado funcional ni certificación.

El canal está en una rama de tarea para validar la lectura anónima, descarga del motor/adaptadores y ejecución desde un ejecutable instalado. No se modifica `main` ni se publica `production.json`. Cada promoción posterior requiere un PR, revisión, firma y generación superior.
