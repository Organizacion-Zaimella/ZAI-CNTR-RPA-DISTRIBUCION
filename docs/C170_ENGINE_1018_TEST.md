# C.170 — motor 1.0.18 en TEST

La generación TEST 99 cambia solo el motor a `1.0.18-test.1`; conserva los doce adaptadores, la lista de revocación y el contrato del canal 98. Fuente RPA: `833ff69d67f6ff552b12b7c704dc0ba61a8d5d1b`.

- Release prerelease: `cntr-rpa-engine-1.0.18-test1`.
- ZIP SHA-256: `16319266336714823dbab646383f4da8cad33b83b9518c201b69214626a5d6aa`.
- Motor dentro del ZIP: versión CLI `1.0.18`, SHA-256 `ce4d1c7dc945407e99fe38cbe9142fa35e20944459084c62c04634a1e88ca155`.
- Lectura anónima HTTP 200 del ZIP, manifest y firma; Ed25519, SHA-256 e inventario aprobados.
- El cambio distingue errores seguros del preflight ORDS y usa la versión compatible del canal firmado aun si la referencia ORDS está atrasada, ausente o mal formada.
- Pruebas locales dirigidas: 115 aprobadas, 4 omitidas; build del motor: 73 aprobadas, 4 omitidas, preflight y sidecar aprobados. La consulta de asignaciones ORDS TEST de solo lectura con la fuente nueva devolvió código 0; no ejecutó documentos.

**Pendiente:** instalación/actualización desde este canal en TEST y corrida documental controlada con evidencia y ACK. La presencia del motor en el canal no acredita esa corrida ni autoriza por sí sola un pase a Producción.
