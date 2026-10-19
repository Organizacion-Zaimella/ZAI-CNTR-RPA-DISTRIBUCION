# C.170 — sesión de navegador, TEST

El motor 1.0.20-test.1 y `ministerio_interior` 0.1.8-candidate proceden del commit RPA `dbcd57442456871ded1fd46c14201ec6525e3b0f`. Los assets están firmados con la clave TEST, publicados en Releases y referenciados por la generación TEST 102. Los otros adaptadores y la lista de revocación se conservan.

Validación previa con los mismos bytes del motor y el módulo de adaptador: ejecución ORDS TEST 1868, detalles 2584 y 2585 `COMPLETADO` y `ACKED`, dos PDF con SHA-256 en el journal; una sesión de navegador iniciada y cerrada al terminar los dos sujetos. El usuario resolvió el CAPTCHA; el adaptador pulsó los avisos y continuó desde el formulario. Las 15 pruebas locales del adaptador y 79 pruebas del motor pasaron; 4 del motor quedaron omitidas.

Las dos corridas de diagnóstico anteriores, 1866 y 1867, acabaron `REINTENTABLE` y permitieron identificar el botón de términos oculto que permanecía en el DOM. Ninguna se usa como evidencia de éxito.

El canal TEST no constituye una publicación productiva. El launcher instalado elegirá el motor y adaptador productivos solo después de la promoción firmada correspondiente.
