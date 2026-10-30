# C.206 — Motor 1.0.29 en canal TEST

- Fuente RPA: `ce8b3ca34e612ec6ccbcd13f95880218d4f92500`.
- Motor construido desde esa fuente: `1.0.29`; suite `87 passed, 4 skipped`; build congelado `V100_BUILD_PASS`, EXE `--version`, preflight Edge/Chrome y sidecar aprobados.
- Release TEST: `cntr-rpa-engine-1.0.29-test.1`; paquete SHA-256 `ce56bfd1af37dbe028451b1b1ec64cbcf1f07d733d36ee13a3679b1bea1c1be7`.
- Canal TEST: generación `127`, derivada de `main` generación `126`; mantiene los 12 adaptadores y revocaciones vigentes.
- `verify_public_channel.py --channel TEST --channel-file ...` aprobó el motor y los 12 adaptadores con descarga pública anónima, manifiestos, firmas, SBOM y ZIP.
- Esta actualización del canal solo pone el motor en TEST. La prueba de auditoría C.206 ya acreditó en ZAITEST el código/causa, recibo GET, idempotencia y compatibilidad legacy; no se ejecutó una consulta real de portal con este EXE firmado.
- PRODUCCIÓN no se modifica en este cambio de canal TEST. El canal productivo se actualizará en un pase separado, después de verificar la candidata y preservar el estado más reciente de `main`.
