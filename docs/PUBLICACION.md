# Política de publicación

1. Desarrollar y revisar el cambio en su repositorio privado, con commit exacto y pruebas de contrato.
2. Verificar que el contenido público no incluya datos personales, evidencias, cookies, tokens, URLs internas ni claves privadas. Confirmar derechos de publicación antes de copiar un adaptador.
3. Construir desde fuente aprobada con dependencias bloqueadas, registrar SBOM, compatibilidad y SHA-256; firmar manifest y artefactos mediante una clave custodiada fuera de este repositorio.
4. Publicar assets en un GitHub Release inmutable, sin sobrescribir tags ni assets existentes. Un build no equivale a release aprobada.
5. Promover canal TEST y luego Producción mediante PR revisado y checks definidos. El puntero firmado se actualiza solo después de que el asset existe y pasa los gates del canal.
6. Documentar revocación y reversión. Una versión retirada no debe ejecutarse por estar en caché.

La rama `main` alberga la documentación base. La rama draft de T07 incorpora un canal TEST de generación 3 y el prerelease candidato `cntr-rpa-1.0.0-test.3`; ambos se usan para QA anónimo de motor y adaptadores. La actualización incluye una corrección del transporte del origen canónico al crear detalles ORDS. Esto no certifica funcionalidad ni aprueba Producción. El control de branch y aprobadores se comprueba por separado; este documento no afirma que estén configurados.

## Candidato TEST generación 7 — 2026-10-09

La rama `codex/sri-0.1.1-test9` prepara el prerelease firmado `cntr-rpa-1.0.0-test.9` desde el canal TEST verificado de generación 6. El canal resultante conserva el motor `1.0.0-test.5` y añade `sri@0.1.1-candidate`; conserva además los candidatos IESS `0.1.2` y OFAC `0.1.1`. El asset SRI incluye `app.py`, `adapter.py`, `dependencies.lock` y manifiesto con punto de entrada standalone declarado, SBOM, firma y hash.

Este candidato corrige la clasificación local de desconexión de red y pasa pruebas sintéticas. La versión ORDS vigente continúa fijada a `sri@0.1.0-candidate`, por lo que la generación 7 no se activa ni prueba su descarga por el robot. La publicación TEST no certifica resultado real del portal, PDF/ACK en ORDS ni Producción. `main` y los canales de Producción no se modifican.

## Candidato TEST generación 8 — SRI 0.1.2 — 2026-10-09

La rama `codex/sri-0.1.2-test10` parte del canal firmado generación 7 y crea generación 8, manteniendo el motor `1.0.0-test.5`, IESS `0.1.2-candidate` y OFAC `0.1.1-candidate`; SRI `0.1.1` se sustituye por `0.1.2-candidate` en este canal inactivo. El nuevo `adapter.py` usa el `type_text` pausado del motor, valida la persistencia del campo y espera a que el botón quede habilitado antes de una sola consulta. Conserva CAPTCHA/ALTCHA como intervención humana. El prerelease `cntr-rpa-1.0.0-test.10` contiene app, sidecar, dependencia fijada, manifiesto, SBOM, hash y firmas TEST.

La compatibilidad corregida pasó pruebas sintéticas del adaptador y standalone. No se hizo E2E de navegación en esta versión ni se produjo evidencia/ACK de esta versión. ORDS sigue fijado a `sri@0.1.0-candidate`; el canal generación 8 no es seleccionable y no se activó. La generación 7 y `sri@0.1.1` permanecen en la rama/historial anterior y no se declara certificación. `main`, ORDS y Producción no se modifican.

## Candidato TEST generación 9 — IESS 0.1.3 — 2026-10-10

La rama `codex/iess-0.1.3-candidate` incorpora `iess@0.1.3-candidate` al canal firmado generación 9 y al prerelease `cntr-rpa-1.0.0-test.11`. El paquete incluye la aplicación independiente y el punto de entrada sidecar. El sidecar delega en esa aplicación para mantener una sola implementación de adquisición y validación PDF. La aplicación standalone obtuvo `MATCH` con PDF nativo estructuralmente válido en una corrida TEST desde el inicio; la suite local terminó 8/8.

Esto es una publicación candidata para QA, no certificación integrada. El pin ORDS vigente continúa en `iess@0.1.0-candidate`; la ejecución del paquete desde el motor instalado con evidencia y ACK ORDS sigue pendiente. `main`, elegibilidad, reglas y Producción no se modifican.

## Candidato TEST generación 10 — SRI 0.1.3 — 2026-10-10

La rama `codex/sri-0.1.3-test12` agrega `sri@0.1.3-candidate` y el prerelease firmado `cntr-rpa-1.0.0-test.12` sobre la generación 9. El cambio aplica la pausa mínima entre navegación y clic del modo de búsqueda; la suite local terminó 11/11. No hubo una consulta pública nueva después de observar `ERR_CONNECTION_RESET`, así que el paquete queda como candidato para QA, sin afirmar que el cambio resuelva ese resultado.

ORDS conserva el pin SRI `0.1.0-candidate`. Esta publicación no cambia elegibilidad ni reglas, no ejecuta el adaptador desde el robot y no cambia `main` ni Producción.
