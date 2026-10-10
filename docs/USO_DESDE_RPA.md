# Uso anónimo desde CNTR RPA

El cliente fijará el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. La lectura de archivos públicos y futuros assets de Releases no requerirá cuenta, token ni cookie de GitHub.

Cuando exista un canal aprobado, el launcher leerá `channels/test.json` o `channels/production.json` junto con su firma `*.sig` por HTTPS. Antes de descargar o ejecutar, verificará firma con clave pública anclada, generación, caducidad, revocación, versión compatible de motor/adaptador, sistema operativo, Playwright/browser, tamaño y SHA-256 de cada asset. Solo descargará assets de Releases del propietario y repositorio fijados. Nunca instalará dependencias mediante `pip` desde Internet durante un arranque.

La instalación usará staging por versión, autochequeo y activación atómica. Conservará configuración, OAuth, journal y logs; ante fallo restaurará la última versión verificada. Si la red falla, aplicará la política autorizada de caché sin ejecutar paquetes revocados ni omitir una actualización de seguridad obligatoria.

**Registro histórico T01:** en la creación inicial no existían canales, firmas ni Releases; ese estado no representa las ramas candidatas posteriores. El canal vigente depende de la rama/release TEST seleccionada explícitamente.

## Lista Clinton 0.1.4 TEST

La rama candidata distribuye la generación 21 con `lista_clinton@0.1.4-candidate`.
El motor solo puede seleccionarla cuando el plan ORDS requiera esa identidad y
versión exactas. El snapshot TEST actual no asigna adaptador ni entrega un par
elegible para documento 33; no se debe forzar la instalación/ejecución. La
versión es TEST y no está aprobada para Producción.
