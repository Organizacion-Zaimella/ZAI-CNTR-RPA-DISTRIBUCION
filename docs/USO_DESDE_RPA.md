# Uso anónimo desde CNTR RPA

**Estado C.145:** TEST generación 36 tiene campaña aprobada para diez documentos. El canal PROD generación 2 distribuye motor 1.0.1 y cinco adaptadores estables; INTERPOL no se habilita. El launcher verifica y descarga la versión firmada de `main` antes de ejecutar. El instalador completo es una entrega separada del actualizador incremental.

El cliente fijará el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. La lectura de archivos públicos y futuros assets de Releases no requerirá cuenta, token ni cookie de GitHub.

El launcher lee el canal permitido para el ambiente y verifica su firma con clave pública anclada, generación, caducidad, revocación, versión compatible de motor/adaptador, sistema operativo, Playwright/browser, tamaño y SHA-256 de cada asset. Solo descarga assets de Releases del propietario y repositorio fijados. Nunca instala dependencias mediante pip desde Internet durante un arranque.

La instalación usará staging por versión, autochequeo y activación atómica. Conservará configuración, OAuth, journal y logs; ante fallo restaurará la última versión verificada. Si la red falla, aplicará la política autorizada de caché sin ejecutar paquetes revocados ni omitir una actualización de seguridad obligatoria.

**Registro histórico T01:** en la creación inicial no existían canales, firmas ni Releases; ese estado no representa las ramas candidatas posteriores. El canal vigente depende de la rama/release TEST seleccionada explícitamente.

## Versión efectiva de una instalación 1.0.0

El `distribution_ref` de la configuración local identifica la rama del canal TEST. El actualizador valida su manifiesto firmado y escribe `state/test/active.json`. El motor efectivo es `engine.path/CNTR-RPA-100.exe` de ese estado, tras comprobar su hash; un EXE de bootstrap o una copia antigua en la raíz no representa la versión activa. El plan ORDS selecciona las versiones exactas de adaptadores y el actualizador exige que figuren en el mismo canal firmado. Para la integración actual, usar [el inventario de la generación 36](../channels/VERSIONES_TEST.md) y registrar la generación activa antes de ejecutar.

## Lista Clinton 0.1.4 TEST

La rama candidata distribuye la generación 21 con `lista_clinton@0.1.4-candidate`.
El motor solo puede seleccionarla cuando el plan ORDS requiera esa identidad y
versión exactas. El snapshot TEST actual no asigna adaptador ni entrega un par
elegible para documento 33; no se debe forzar la instalación/ejecución. La
versión es TEST y no está aprobada para Producción.


## INTERPOL 0.1.1 TEST candidate

El canal 36 distribuye `interpol@0.1.1-candidate`, migración técnica del workflow 61/v2 para documento 12. Se verificó firma e integridad del paquete. La ejecución validada usa fixtures de loopback; toda URL externa sigue bloqueada por `INTERPOL_WRITTEN_PERMISSION_REQUIRED`. No hay consulta real ni ACK ORDS.
