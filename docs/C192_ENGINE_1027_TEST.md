# C.192 — motor 1.0.27 en TEST

- Canal firmado TEST: generación 113, motor `1.0.27-test.1`; las 12 asignaciones de adaptadores y las revocaciones de la generación 112 se conservan.
- Fuente del motor: `34bb6e8ea0b430adb38f0dab34f5e9a2548aad99`, integrado mediante PR RPA #70.
- La release pública `cntr-rpa-engine-1.0.27-test1` contiene ZIP, manifiesto, firma y SBOM; los cuatro assets respondieron HTTP 200 antes de actualizar el canal.
- QA de la lógica: 138 pruebas aprobadas, 4 omitidas; ejecutable congelado `1.0.27` y sidecar verificados.
- QA real ORDS TEST: configuración 659, ejecución 1949, detalle 2667, OFAC documento 5. Se simuló la pérdida de la respuesta tras guardar el resultado en ORDS; el motor consultó el resultado, reconcilió el ACK y terminó. Oracle TEST confirmó ejecución `COMPLETADA`, detalle `SIN_RESULTADO`, evidencia 89 y clave de resultado persistida.
- El incidente productivo 1605 no expone el código HTTP ni la etapa del fallo original; esta actualización hace visible esa información en el diagnóstico privado de futuras corridas.
