# C.206 — Motor 1.0.29 en Producción

- Código RPA: `ce8b3ca34e612ec6ccbcd13f95880218d4f92500`.
- Release estable: `cntr-rpa-engine-1.0.29`.
- Binario: `cntr-rpa-engine-1.0.29-win-x64.zip`.
- SHA-256 del ZIP: `9b773fb6df831ea543c453c3ef355a53545e9a7189e6e2f804a46915fa5458e5`.
- SHA-256 del ejecutable: validado contra el candidato TEST firmado.
- El canal TEST generación 127 (motor `1.0.29-test.1`) pasó el verificador público para sus 13 componentes.
- El canal PRODUCCIÓN candidato generación 36 reemplaza únicamente el motor; conserva 10 adaptadores y 4 revocaciones de la generación 35.
- SHA-256 del canal candidato: `f24d5e0838c55d0b33a29ff3471f8bd742aeb50950e307f0ac858c44303e66d7`.
- La evidencia del gate del canal candidato queda en `docs/tareas/C.206/logs/verify-production-candidate.json` del contexto del proyecto.
- No se ejecutó una corrida documental ni pruebas HTTP en Producción. ORDS `rc.11` fue desplegado con el SQL de C.206 desde el commit Oracle integrado `e540a26eeb9d2d9a60aa9b374472dd108c4d1290`.

La activación ocurre cuando este canal firmado se integre a `main`. Los launchers instalados consumen la nueva generación al iniciarse; no requieren reinstalación.
