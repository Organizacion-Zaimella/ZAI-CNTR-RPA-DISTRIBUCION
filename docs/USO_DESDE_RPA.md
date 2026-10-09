# Uso anónimo desde CNTR RPA

El cliente fijará el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. La lectura de archivos públicos y futuros assets de Releases no requerirá cuenta, token ni cookie de GitHub.

Cuando exista un canal aprobado, el launcher leerá `channels/test.json` o `channels/production.json` junto con su firma `*.sig` por HTTPS. Antes de descargar o ejecutar, verificará firma con clave pública anclada, generación, caducidad, revocación, versión compatible de motor/adaptador, sistema operativo, Playwright/browser, tamaño y SHA-256 de cada asset. Solo descargará assets de Releases del propietario y repositorio fijados. Nunca instalará dependencias mediante `pip` desde Internet durante un arranque.

La instalación usará staging por versión, autochequeo y activación atómica. Conservará configuración, OAuth, journal y logs; ante fallo restaurará la última versión verificada. Si la red falla, aplicará la política autorizada de caché sin ejecutar paquetes revocados ni omitir una actualización de seguridad obligatoria.

**Estado T01:** no hay canales, firmas ni Releases; cualquier GET a esas rutas futuras puede devolver 404 y no debe interpretarse como actualización disponible. Solo el README y este documento se usan ahora para comprobar lectura anónima.
