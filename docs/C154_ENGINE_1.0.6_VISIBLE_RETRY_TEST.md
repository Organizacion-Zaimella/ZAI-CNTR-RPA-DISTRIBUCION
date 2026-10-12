# C.154 — motor 1.0.6 TEST con reintento visible

## Estado del candidato

- Canal propuesto: TEST, generación 66.
- Motor: `1.0.6-test.1` (versión de CLI `1.0.6`).
- Commit del código RPA: `7bf632650ecf0988c36000a8fbdf99a8f492939c`.
- Release: `cntr-rpa-engine-1.0.6-test.1`.
- Clave de firma: `cntr-test-a37738608946` (TEST).
- Adaptadores: se conservan las doce asignaciones de la generación TEST 65.

## Cambio

Cuando un trabajo automático termina en navegador oculto (`HEADLESS` o `BACKGROUND`) con `PORTAL_UNAVAILABLE` o `ACTION_TIMEOUT`/`PORTAL_TIMEOUT`, el motor vuelve a ejecutar ese mismo documento una vez en navegador visible, antes de persistir el resultado y enviar ACK. Mantiene los identificadores y generación ORDS, registra un solo resultado final y continúa el plan si el segundo intento falla. No reintenta resultados concluyentes, barreras humanas ni errores de contrato/adaptador.

## Evidencia técnica

- `tests/test_v100_motor.py`: incluye recuperación visible positiva con evidencia/ACK, timeout, caída de red y continuidad del siguiente detalle.
- Resultado local: 53 pruebas aprobadas y 4 omitidas por requerir instalaciones privadas/aisladas.
- El EXE PyInstaller `1.0.6` pasó preflight y la prueba de sidecar con adaptador externo.
- El paquete y los manifiestos se validaron con la clave TEST y la firma/hash de canal.
- No se consultaron portales ni se generaron ejecuciones documentales ORDS.

## Límite

Este candidato no modifica la generación de Producción 7 (motor 1.0.5). Requiere integrar este PR para que el puntero de TEST en `main` avance. Una instalación de prueba puede apuntar temporalmente a la rama candidata `codex/c154-visible-retry`; seleccionar Producción con este instalador conservará el canal productivo vigente y no activa este motor.
