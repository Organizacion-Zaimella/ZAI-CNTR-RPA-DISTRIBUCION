# Uso anónimo desde CNTR RPA

El cliente fijará el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. La lectura de archivos públicos y futuros assets de Releases no requerirá cuenta, token ni cookie de GitHub.

El canal TEST de esta rama es un candidato de QA firmado, sin aprobación de Producción. El launcher lee `channels/test.json` junto con su firma `.sig` por HTTPS. Antes de descargar o ejecutar, verifica firma con clave pública anclada, generación, caducidad, revocación, compatibilidad de motor/adaptador, sistema operativo, Playwright/browser, tamaño y SHA-256 de cada asset. Solo descarga assets de Releases del propietario y repositorio fijados. Nunca instala dependencias mediante `pip` desde Internet durante un arranque.

La instalación usará staging por versión, autochequeo y activación atómica. Conservará configuración, OAuth, journal y logs; ante fallo restaurará la última versión verificada. Si la red falla, aplicará la política autorizada de caché sin ejecutar paquetes revocados ni omitir una actualización de seguridad obligatoria.

No existe canal `production.json`; ningún candidato de TEST autoriza ejecución o actualización en Producción. Los adaptadores de la generación 2 están pendientes de QA E2E instalado con evidencia y ACK.
