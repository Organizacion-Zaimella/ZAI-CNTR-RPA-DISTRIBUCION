# Uso anónimo desde CNTR RPA

El cliente fijará el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. La lectura de archivos públicos y futuros assets de Releases no requerirá cuenta, token ni cookie de GitHub.

La rama candidata `codex/iess-0.1.3-candidate` contiene un canal TEST firmado de generación 9 y prerelease `cntr-rpa-1.0.0-test.11`; el motor es `1.0.0-test.5` y los candidatos incluyen IESS `0.1.3`, OFAC `0.1.1` y SRI `0.1.2`. Es opt-in por referencia explícita de rama y no tiene aprobación de Producción. ORDS todavía asigna IESS `0.1.0-candidate`, por lo que `0.1.3` no se selecciona para el plan actual hasta actualizar su asignación TEST. El launcher lee `channels/test.json` junto con su firma `.sig` por HTTPS. Antes de descargar o ejecutar, verifica firma con clave pública anclada, generación, caducidad, revocación, compatibilidad de motor/adaptador, sistema operativo, Playwright/browser, tamaño y SHA-256 de cada asset. Solo descarga assets de Releases del propietario y repositorio fijados. Nunca instala dependencias mediante `pip` desde Internet durante un arranque.

La instalación usará staging por versión, autochequeo y activación atómica. Conservará configuración, OAuth, journal y logs; ante fallo restaurará la última versión verificada. Si la red falla, aplicará la política autorizada de caché sin ejecutar paquetes revocados ni omitir una actualización de seguridad obligatoria.

No existe canal `production.json`; ningún candidato de TEST autoriza ejecución o actualización en Producción. Los adaptadores de generación 7 siguen pendientes de QA E2E por versión instalada, evidencia y ACK.
