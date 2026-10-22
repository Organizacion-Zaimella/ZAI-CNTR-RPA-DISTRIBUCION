# C.192 — motor 1.0.27 en Producción

- Cambio: generación 29, motor `1.0.27`; conserva los diez adaptadores y las revocaciones de generación 28.
- Origen: fuente RPA `34bb6e8ea0b430adb38f0dab34f5e9a2548aad99`, integrada en `origin/main`; ejecutable idéntico por SHA-256 al candidato firmado TEST `1.0.27-test.1` de generación 113.
- QA: 138 pruebas aprobadas y cuatro omitidas; build congelado 1.0.27; ejecución TEST 1949/detalle 2667 terminó con ACK reconciliado tras simular pérdida de la respuesta. Oracle TEST confirmó detalle, evidencia 89 y resultado persistido.
- Publicación: release `cntr-rpa-engine-1.0.27` con ZIP, manifiesto, firma y SBOM, los cuatro assets HTTP 200 antes de activar el canal productivo.
- Efecto: el launcher instalado descarga el nuevo motor al iniciar. El log privado distinguirá etapa, motivo y estado HTTP de futuros ACK pendientes y el resumen solo contará como éxito los resultados confirmados.
- Límite: el log de la ejecución productiva 1605 no incluyó la causa HTTP exacta; no se ha repetido esa ejecución como parte del pase.
