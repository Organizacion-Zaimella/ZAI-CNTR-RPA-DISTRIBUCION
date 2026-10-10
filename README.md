# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Canal TEST de esta rama:** generación 21, publicada como candidato el 10 de octubre de 2026. Incluye `lista_clinton@0.1.4-candidate` para portal 5/documento 33, junto con los adaptadores enumerados en el manifiesto firmado.

La versión firmada anterior 0.1.3 valida la descarga del PDF, el paquete y la carga dinámica. El candidato 0.1.4 acota la salida cuando una frase aparece en muchas páginas; el procesamiento local del PDF completo dio un bundle PDF válido. No se ejecutó búsqueda de sujetos porque el plan ORDS no contiene pares elegibles ni asignación para doc. 33; no existe ACK ni certificación funcional integral.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Todo asset es un candidato de TEST, no una autorización para Producción.
