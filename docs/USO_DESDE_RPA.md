# Uso anónimo desde CNTR RPA

El cliente fijará el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. La lectura de archivos públicos y futuros assets de Releases no requerirá cuenta, token ni cookie de GitHub.

La rama candidata `codex/sri-0.1.3-test12` contiene un canal TEST firmado de generación 10 y prerelease `cntr-rpa-1.0.0-test.12`; el motor es `1.0.0-test.5` y los candidatos incluyen IESS `0.1.3`, OFAC `0.1.1` y SRI `0.1.3`. Es opt-in por referencia explícita de rama y no tiene aprobación de Producción. ORDS todavía asigna `0.1.0-candidate` para IESS y SRI, por lo que las versiones nuevas no se seleccionan hasta actualizar sus asignaciones TEST. El launcher lee `channels/test.json` junto con su firma `.sig` por HTTPS. Antes de descargar o ejecutar, verifica firma con clave pública anclada, generación, caducidad, revocación, compatibilidad de motor/adaptador, sistema operativo, Playwright/browser, tamaño y SHA-256 de cada asset. Solo descarga assets de Releases del propietario y repositorio fijados. Nunca instala dependencias mediante `pip` desde Internet durante un arranque.

La instalación usará staging por versión, autochequeo y activación atómica. Conservará configuración, OAuth, journal y logs; ante fallo restaurará la última versión verificada. Si la red falla, aplicará la política autorizada de caché sin ejecutar paquetes revocados ni omitir una actualización de seguridad obligatoria.

No existe canal `production.json`; ningún candidato de TEST autoriza ejecución o actualización en Producción. Los adaptadores de generación 7 siguen pendientes de QA E2E por versión instalada, evidencia y ACK.
# SRI 0.1.12 — uso del candidato TEST

La release firmada `cntr-rpa-sri-0.1.12-test20` se publicó como candidato TEST
y la generación 20 incorpora esa versión. La ejecución autónoma validada fue
standalone; no es una instrucción para forzarla desde el robot. Antes de usar el
canal, confirmar que el plan ORDS de TEST entrega exactamente la misma versión.
La lectura vigente todavía devuelve `sri@0.1.8-candidate`, por lo que la
integración del candidato queda pendiente y esta versión no debe desplegarse en
Producción.
