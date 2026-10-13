# C.155 — candidatos técnicos TEST

Canal TEST generación 71: motor `1.0.8-test.1`, Ministerio del Interior `0.1.3-candidate` y Fiscalía `0.1.5-candidate`. Las demás asignaciones del canal 67 se conservan. Fuente del motor y Fiscalía: RPA `91e387bb42507b798fcb8016f14b9e958533ec3f`; fuente de Ministerio 0.1.3: `47af3ae0f80a9c449b2554f30e0b013e4da5451d`. La generación 70 con Ministerio 0.1.2 fue un candidato previo y no se modifica su release inmutable.

- Ministerio: recupera en la misma sesión el formulario y la pestaña PDF. Se obtuvo un PDF real válido por la función Python independiente en una sesión atendida. En una corrida nueva el CAPTCHA se resolvió, pero el portal mantuvo el indicador “Por favor espere…” tras enviar identificación. La versión 0.1.3 espera ese estado válido hasta un límite de tres minutos por intento, sin reenviar la consulta. Faltan resultado concluyente y ACK del robot; no se declara certificación.
- Fiscalía: incorpora captura verificada de todo el iframe con mosaicos de desplazamiento, derivada del workflow histórico. Los escenarios locales positivos y negativos pasaron; falta la prueba real de esta versión y el ACK instalado.
- Motor: agrega adquisición genérica de PDF en pestaña hija, captura completa de iframe y clasificación explícita de errores. Build PyInstaller y prueba de sidecar externo aprobados localmente. El motor no contiene navegación específica de estos portales.
- Superintendencia documento 16 permanece pendiente por indisponibilidad externa observada. No se publica nueva versión de ese adaptador en esta generación.

Los tres assets se publican como Releases de TEST, separados del código y firmados. La versión autorizada para cada trabajo sigue llegando por ORDS; el canal firmado debe contener un paquete compatible. Ningún candidato de este expediente autoriza el pase a Producción ni sustituye evidencia y ACK de una corrida real.
