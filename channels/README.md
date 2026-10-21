# Canales de distribución

C.178 activa TEST generación 108 con Judicatura 0.1.8-candidate y Lista Clinton 0.1.5-candidate. Ambos adaptadores definen y validan su URL de entrada y no dependen de `work.entry_url`. Mantiene el motor TEST 1.0.24-test.1 y no modifica el canal de Producción (motor 1.0.24). ORDS asigna actualmente el documento 33 a `ofac`; Lista Clinton no se promueve ni se asigna por esta tarea.

C.170 publica PRODUCCIÓN generación 18 con motor `1.0.18`; conserva los diez adaptadores de la generación 17. El launcher con diagnóstico ORDS legible se distribuye en el instalador 1.0.8. Véase [el pase y sus límites](../docs/C170_ENGINE_1018_PRODUCTION.md).

C.170 propone TEST generación 99 y motor `1.0.18-test.1` con diagnóstico legible del preflight ORDS y selección de versión firmada independiente de la referencia documental de ORDS. Conserva los doce adaptadores de la generación 98. Véase [la evidencia del candidato](../docs/C170_ENGINE_1018_TEST.md).

`test.json` y `test.json.sig` son el puntero y la firma vigentes del canal TEST; `production.json` y su firma cumplen el mismo papel para Producción. El [inventario TEST](VERSIONES_TEST.md) se deriva del JSON firmado. Los resúmenes históricos de otras generaciones permanecen en Git.

C.156 propone la generación TEST 84 con las aplicaciones `servicios_educacion@0.1.1-candidate` y `senescyt@0.1.1-candidate`. Son paquetes independientes del motor. ORDS decide qué versión recibe cada documento; el canal solo ofrece versiones verificables y no altera elegibilidad, resultados ni permisos. Las pruebas reales y los ACK deben acreditarse por separado.

C.157 verificó la generación TEST 89 mediante instalación aislada: ejecución 1826, detalle 2540, documento 16 `COMPLETADO` con evidencia y ACK en Oracle TEST. La generación 11 de Producción propone motor 1.0.11 y Supercias 0.1.17 desde los mismos bytes probados; conserva todos los demás adaptadores de la generación 10. El canal productivo sólo entra en vigor al integrar el cambio de `production.json` y su firma a `main`.

La generación TEST 90 añade SENESCYT 0.1.4-candidate para estabilizar la identificación tras una sustitución tardía del formulario JSF. No cambia el canal de Producción ni el motor.

C.158 publica motor 1.0.13 en generación 13 de Producción. Incorpora la recuperación en primer plano de documentos automáticos que terminen sin progreso verificable y registra el inicio efectivo de cada detalle; conserva las diez versiones de adaptadores del canal anterior. El canal fue firmado después de validar en TEST la actualización de una instalación existente y una corrida real de Judicatura con dos evidencias y dos ACK.

C.159 publica la generación 14 de Producción con motor 1.0.14 y `ministerio_interior@0.1.7`. El motor recupera una pestaña tras timeout sin reutilizar el resultado del detalle anterior. El adaptador ata el checkpoint al detalle y verifica la identificación extraída del PDF antes de aceptarlo. En TEST, la ejecución instalada 1847 completó dos sujetos consecutivos del documento 4 con dos PDFs y dos ACK; se comprobó en privado que cada PDF contiene la identificación de su propio sujeto. Los otros nueve adaptadores y la lista de revocación permanecen iguales a la generación 13. La invalidación de evidencias históricas ajenas sigue el permiso del propietario en Oracle y no forma parte de este canal.
