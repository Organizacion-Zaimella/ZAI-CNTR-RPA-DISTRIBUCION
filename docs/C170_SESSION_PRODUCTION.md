# C.170 — sesión de navegador, Producción

El canal firmado Producción generación 20 actualiza el motor a 1.0.20 y `ministerio_interior` a 0.1.8. Conserva las demás asignaciones y revocaciones de la generación 19. El launcher instalado verifica firma, SHA-256 y compatibilidad y descarga estas versiones al volver a ejecutarse; no se requiere reinstalación.

Fuente RPA del motor y adaptador: `dbcd57442456871ded1fd46c14201ec6525e3b0f`. El generador de promoción versionado verificó el binario exacto del motor firmado en TEST generación 102 y descargó el paquete TEST del adaptador comprobando tamaño y SHA-256. Los nuevos Releases productivos y manifiestos están firmados con la clave de Producción.

Validación real previa: ORDS TEST ejecución 1868, detalles 2584/2585 `COMPLETADO` y `ACKED`, ambos con PDF y una sola sesión de navegador. El CAPTCHA lo resolvió el usuario. No se hizo QA funcional sobre datos de Producción. Las corridas de diagnóstico anteriores quedaron `REINTENTABLE` y no se usan para afirmar éxito.

Si se necesita revertir, publicar una nueva generación firmada que vuelva a apuntar al motor 1.0.19 y al adaptador 0.1.7, tras verificar sus Releases. No degradar ni sobrescribir la generación 20 en cachés o tags existentes.
