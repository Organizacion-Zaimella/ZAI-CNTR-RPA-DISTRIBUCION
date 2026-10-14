# Canales de distribución

`test.json` y `test.json.sig` son el puntero y la firma vigentes del canal TEST; `production.json` y su firma cumplen el mismo papel para Producción. El [inventario TEST](VERSIONES_TEST.md) se deriva del JSON firmado. Los resúmenes históricos de otras generaciones permanecen en Git.

C.156 propone la generación TEST 84 con las aplicaciones `servicios_educacion@0.1.1-candidate` y `senescyt@0.1.1-candidate`. Son paquetes independientes del motor. ORDS decide qué versión recibe cada documento; el canal solo ofrece versiones verificables y no altera elegibilidad, resultados ni permisos. Las pruebas reales y los ACK deben acreditarse por separado.

C.157 ofrece la generación TEST 89 para verificar el motor 1.0.11 y Supercias 0.1.17. No promover estos candidatos a Producción sin evidencia y ACK desde la instalación de TEST.
