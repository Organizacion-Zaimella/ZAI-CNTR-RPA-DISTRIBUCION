# C.204 — Supercias y motor en PRODUCCIÓN

- Canal firmado: generación 35; motor 1.0.28 y adaptador `supercias@0.1.29`.
- Motor: ejecutable idéntico al probado en TEST, procedente del commit `51a0b00d5669559804b95f66d0d0b0e2435e54e8`; amplía el tiempo disponible para la intervención humana.
- Supercias: paquete promovido desde `0.1.29-candidate`, commit `20d85bc36c4c8f4fde9556cf028faf46cb2b0e53`. Selecciona una fila ante fechas empatadas, guarda el balance disponible si falta el año anterior y continúa tras errores de documentos o avisos de PDF firmado.
- TEST: ejecuciones 2057/2058, cuatro ACK, dos balances completados con evidencia y dos errores esperados por PDF firmado. Suite Supercias: 61 aprobadas; suite motor: 86 aprobadas y 4 omitidas.
- Previo a la activación se publicaron los releases `cntr-rpa-engine-1.0.28` y `cntr-rpa-supercias-0.1.29`, con ZIP, `release-manifest.json`, `release-manifest.json.sig` y `sbom.json`. La comprobación pública anónima del canal candidato pasó para los 11 componentes.
- Los launchers instalados descargan el motor y adaptador firmados al iniciar. Las pruebas documentales funcionales se realizaron en TEST.