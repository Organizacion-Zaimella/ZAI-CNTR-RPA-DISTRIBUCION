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
