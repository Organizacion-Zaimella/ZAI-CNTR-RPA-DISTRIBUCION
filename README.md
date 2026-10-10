# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Canal TEST de esta rama:** generación 22, candidata del 10 de octubre de 2026. Incluye `lista_clinton@0.1.4-candidate` y `consejo_judicatura@0.1.2-candidate`, junto con los adaptadores enumerados en el manifiesto firmado.

La versión firmada anterior 0.1.3 valida la descarga del PDF, el paquete y la carga dinámica. El candidato 0.1.4 acota la salida cuando una frase aparece en muchas páginas; el procesamiento local del PDF completo dio un bundle PDF válido. No se ejecutó búsqueda de sujetos porque el plan ORDS no contiene pares elegibles ni asignación para doc. 33; no existe ACK ni certificación funcional integral.

Judicatura 0.1.2 obtuvo `NO_MATCH` con PNG privada válida para los documentos 73 y 74 en prueba standalone headed y pasó 14 pruebas sintéticas. El plan ORDS vigente no asigna función ni elegibilidad a Judicatura; el candidato no se declara certificado por robot y no tiene ACK ORDS.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Todo asset es un candidato de TEST, no una autorización para Producción.
