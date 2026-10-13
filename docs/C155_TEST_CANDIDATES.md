# C.155 — candidatos técnicos TEST

Canal TEST generación 70: motor `1.0.8-test.1`, Ministerio del Interior `0.1.2-candidate` y Fiscalía `0.1.5-candidate`. Las demás asignaciones del canal 67 se conservan. Fuente RPA exacta: `91e387bb42507b798fcb8016f14b9e958533ec3f`.

- Ministerio: recupera en la misma sesión el formulario y la pestaña PDF. Se obtuvo un PDF real válido por la función Python independiente en una sesión atendida. Una corrida completa nueva quedó en `HUMAN_REQUIRED` por CAPTCHA sin resolver; no se declara certificación ni ACK del robot para esta versión.
- Fiscalía: incorpora captura verificada de todo el iframe con mosaicos de desplazamiento, derivada del workflow histórico. Los escenarios locales positivos y negativos pasaron; falta la prueba real de esta versión y el ACK instalado.
- Motor: agrega adquisición genérica de PDF en pestaña hija, captura completa de iframe y clasificación explícita de errores. Build PyInstaller y prueba de sidecar externo aprobados localmente. El motor no contiene navegación específica de estos portales.
- Superintendencia documento 16 permanece pendiente por indisponibilidad externa observada. No se publica nueva versión de ese adaptador en esta generación.

Los tres assets se publican como Releases de TEST, separados del código y firmados. La versión autorizada para cada trabajo sigue llegando por ORDS; el canal firmado debe contener un paquete compatible. Ningún candidato de este expediente autoriza el pase a Producción ni sustituye evidencia y ACK de una corrida real.
