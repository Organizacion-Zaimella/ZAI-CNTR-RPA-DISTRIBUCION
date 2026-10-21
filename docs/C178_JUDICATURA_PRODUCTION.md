# C.178 — Consejo de la Judicatura 0.1.8 en Producción

## Estado

La release firmada `cntr-rpa-consejo_judicatura-0.1.8` está publicada. La generación 25 del canal productivo se activa cuando el cambio de `channels/production.json` y su firma se integre en `main`.

## Contenido

- Fuente RPA: `3e4e1e419845403372eabc2ecc2517839c1b4ad5`.
- Package ORDS probado: `DATA.PK_CNTR_ORDS` `1.0.0-rc.9`; SQL SHA-256 `63B9212391DED3563D64A95454A2221EE81CB1765087A4EFF13F21C059C9F891`.
- Adaptador: `consejo_judicatura@0.1.8`, release `cntr-rpa-consejo_judicatura-0.1.8`.
- ZIP firmado: `cntr-rpa-adapter-consejo_judicatura-0.1.8-win-x64.zip`, SHA-256 `c8066993f439eb9ff0196a5845aba737a963e1b23e8ed0b8e789ee090ac3831a`.
- Canal anterior: generación 24; canal candidato: generación 25.
- Motor conservado sin cambios: `1.0.24`, SHA-256 `b50b41d576468973ce735f47ac2b04a3b7607e92fc4f1bdc7c7ca22eb485c374`.
- Firma del canal validada con la clave restringida a `PRODUCCION`; hash del JSON firmado `f7de602f9c8aab87276c073f303faee5fd3835710c8b03d481c117427588466a`.

## Cambio funcional

Consejo define y valida su URL de entrada en su aplicación Python para las funciones 73–76. El adaptador ignora `work.entry_url` y mantiene la barrera CAPTCHA como `HUMAN_REQUIRED`. El motor no se reconstruyó ni se requiere reinstalar el launcher.

ORDS deja de usar los pasos del documento para filtrar trabajos o decidir la URL de navegación. Conserva la elegibilidad por asignación, modalidad, aplicabilidad y vigencia, y entrega `PORTAL_BASE` solo como metadata compatible.

Lista Clinton queda publicada como candidato TEST, fuera del canal productivo. ORDS todavía asigna el documento 33 a `ofac`; esta tarea no cambia la asignación. La aplicación `ofac` ya define su `START_URL` para ese documento.

## QA

- Suite de adaptadores, contrato del motor y distribución: `59 passed`.
- ORDS TEST `rc.9`: package válido; 51 templates y 56 handlers; OAuth anónimo 401, token correcto y autenticado 200.
- Planes GET con configuraciones TEST existentes: 82 trabajos inspeccionados; documentos 73–76 elegibles bajo `consejo_judicatura` y documentos 17–19 no bloqueados por pasos sin URL.
- Ejecución real acotada TEST: configuración existente 637, ejecución 1926, detalle 2640, documento 73; resultado `SIN_RESULTADO`, evidencia registrada y `ACKED`.
- No se creó configuración, sujeto, paso ni asignación para la prueba. La corrida acotada no certifica por sí sola todos los escenarios de los documentos 73–76.

## Publicación y límites

La release de Judicatura y la generación 25 son componentes separados del motor 1.0.24. Al integrarse el canal productivo, el launcher existente descargará el adaptador firmado en su siguiente inicio; no es necesario reinstalar el robot. No iniciar una corrida masiva como parte del pase.
