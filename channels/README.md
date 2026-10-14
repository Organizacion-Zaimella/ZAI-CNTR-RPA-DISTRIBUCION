# Canales de distribución

`test.json` y `test.json.sig` son el puntero y la firma vigentes del canal TEST; `production.json` y su firma cumplen el mismo papel para Producción. El [inventario TEST](VERSIONES_TEST.md) se deriva del JSON firmado. Los resúmenes históricos de otras generaciones permanecen en Git.

C.156 propone la generación TEST 84 con las aplicaciones `servicios_educacion@0.1.1-candidate` y `senescyt@0.1.1-candidate`. Son paquetes independientes del motor. ORDS decide qué versión recibe cada documento; el canal solo ofrece versiones verificables y no altera elegibilidad, resultados ni permisos. Las pruebas reales y los ACK deben acreditarse por separado.

C.157 verificó la generación TEST 89 mediante instalación aislada: ejecución 1826, detalle 2540, documento 16 `COMPLETADO` con evidencia y ACK en Oracle TEST. La generación 11 de Producción propone motor 1.0.11 y Supercias 0.1.17 desde los mismos bytes probados; conserva todos los demás adaptadores de la generación 10. El canal productivo sólo entra en vigor al integrar el cambio de `production.json` y su firma a `main`.

La generación TEST 90 añade SENESCYT 0.1.4-candidate para estabilizar la identificación tras una sustitución tardía del formulario JSF. No cambia el canal de Producción ni el motor.

C.158 publica motor 1.0.13 en generación 13 de Producción. Incorpora la recuperación en primer plano de documentos automáticos que terminen sin progreso verificable y registra el inicio efectivo de cada detalle; conserva las diez versiones de adaptadores del canal anterior. El canal fue firmado después de validar en TEST la actualización de una instalación existente y una corrida real de Judicatura con dos evidencias y dos ACK.
