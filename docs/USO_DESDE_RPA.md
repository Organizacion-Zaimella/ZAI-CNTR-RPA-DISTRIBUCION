# Uso anónimo desde CNTR RPA

El cliente fijará el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. La lectura de archivos públicos y futuros assets de Releases no requerirá cuenta, token ni cookie de GitHub.

La rama candidata vigente `codex/sri-0.1.2-test10` contiene un canal TEST firmado de generación 8 y prerelease `cntr-rpa-1.0.0-test.10`; el motor es `1.0.0-test.5` y los candidatos incluyen IESS/OFAC/SRI. Es opt-in por referencia explícita de rama y no tiene aprobación de Producción. ORDS aún asigna SRI `0.1.0-candidate`; el paquete SRI `0.1.2` no es seleccionable por ese plan hasta una asignación autorizada. El launcher lee `channels/test.json` junto con su firma `.sig` por HTTPS. Antes de descargar o ejecutar, verifica firma con clave pública anclada, generación, caducidad, revocación, compatibilidad de motor/adaptador, sistema operativo, Playwright/browser, tamaño y SHA-256 de cada asset. Solo descarga assets de Releases del propietario y repositorio fijados. Nunca instala dependencias mediante `pip` desde Internet durante un arranque.

La instalación usará staging por versión, autochequeo y activación atómica. Conservará configuración, OAuth, journal y logs; ante fallo restaurará la última versión verificada. Si la red falla, aplicará la política autorizada de caché sin ejecutar paquetes revocados ni omitir una actualización de seguridad obligatoria.

No existe canal `production.json`; ningún candidato de TEST autoriza ejecución o actualización en Producción. Los adaptadores de generación 7 siguen pendientes de QA E2E por versión instalada, evidencia y ACK.
