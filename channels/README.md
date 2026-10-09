# Canales

`test.json` y `test.json.sig` se publican para probar la distribución del motor 1.0.0 en canal TEST. El manifiesto usa generación monotónica y apunta al prerelease firmado `cntr-rpa-engine-1.0.0-test.1`. Este candidato incluye únicamente el motor, sin adaptadores.

El canal está en una rama de tarea para validar la lectura anónima y la descarga desde un ejecutable instalado. No se modifica `main` ni se publica `production.json`. Cada promoción posterior requiere un PR, revisión, firma y generación superior.
