# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Canal TEST:** generación 19, publicada el 10 de octubre de 2026. Incluye el candidato `lista-clinton` 0.1.3 para portal 5/documento 33, además de los adaptadores ya enumerados en el manifiesto firmado.

El candidato Lista Clinton valida descarga pública del PDF de Treasury, bytes, firma `%PDF-`, empaquetado, hashes y resolución del ABI desde el motor. No se ejecutó búsqueda de sujetos, porque el plan ORDS de solo lectura no contenía pares elegibles; no existe ACK ni certificación funcional integral.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Todo asset es un candidato de TEST, no una autorización para Producción.
