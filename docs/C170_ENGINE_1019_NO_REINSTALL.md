# C.170 — diagnóstico del motor sin reinstalación

La generación TEST 100 selecciona el motor `1.0.19-test.1` y conserva los doce adaptadores de la generación 99. El motor escribe `logs/engine-preflight-AAAA-MM-DD.jsonl` cuando falla la consulta de asignaciones ORDS. Cada registro contiene hora, código seguro, explicación y acción recomendada; no guarda URL, credenciales ni datos del sujeto.

- Fuente RPA: `bf62a0c1ab727ce6a2bd11f7b9a1c620ee6702e5` (PR #60).
- Release TEST: `cntr-rpa-engine-1.0.19-test1`; ZIP SHA-256 `faef34aa009ce5a6aaf993a6708ad85c92edb1f4a98529883f35355380b4b0cc`.
- Pruebas: 95 aprobadas, 4 omitidas; build del motor con 73 aprobadas, 4 omitidas, preflight y sidecar aprobados.
- El código del launcher anterior actualizó en sandbox el motor y resolvió seis adaptadores contra ORDS TEST mediante consultas de solo lectura: `TEST_OLD_LAUNCHER_PASS 100 1.0.19-test.1 6`. No se ejecutaron documentos.
- El binario congelado escribió el log local esperado ante configuración sintética inválida y mantuvo el código de salida 3 y el protocolo de stdout del launcher anterior.

La corrida documental de MRGUILLCA, la evidencia y los ACK siguen pendientes. El launcher anterior continuará mostrando su mensaje genérico si falla el preflight; el detalle legible estará en el log privado del motor.
