# C.154 — Motor 1.0.7 para configuraciones mixtas en TEST

El canal TEST generación 67 propone el motor `1.0.7-test.1`, construido desde el
commit RPA `a8994a71194163c28a4f852a44906ad3267d3ff9`.

## Corrección

- Consume conjuntamente `automation_eligible` y `attended_eligible` del plan ORDS.
- Mantiene ocultos los trabajos automáticos y abre visibles los documentos atendidos
  con CAPTCHA/ALTCHA.
- Conserva el orden de ORDS y crea una sola ejecución con todos los pares pendientes
  de una configuración mixta.
- Separa los lotes de navegador automáticos y atendidos.
- Persiste el origen de evidencia `AUTOMATICA` o `ASISTIDA` también durante la
  recuperación de ACK.
- Mantiene el reintento visible único de 1.0.6 para fallos transitorios ocultos.

Las doce versiones de adaptadores del canal TEST 66 se conservan sin cambios. La
ausencia de `attended_eligible` en una revisión ORDS anterior equivale a `false`, por
lo que el motor conserva compatibilidad sin habilitar documentos atendidos por
inferencia.

## Integridad

El ZIP, el manifiesto de release, el SBOM y el canal están firmados con la clave
exclusiva de TEST. La publicación habilita descarga y validación técnica; la
certificación funcional requiere una ejecución real con resultado, evidencia y ACK
para documentos automáticos y atendidos.
