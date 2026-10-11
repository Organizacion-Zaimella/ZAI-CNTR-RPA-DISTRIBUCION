# Releases

Los paquetes firmados se distribuyen como assets de GitHub Releases junto con manifiesto, digests, SBOM, compatibilidad y procedencia. El canal TEST acredita los resultados de la campaña TEST descrita en su expediente, no una certificación legal general. La generación PROD 1 de C.145 contiene motor 1.0.0 y cinco adaptadores estables que cubren diez documentos; INTERPOL se excluye por no tener prueba real certificada. Sus releases y la promoción del puntero requieren disponibilidad verificable de todos los assets y revisión de sus PR.

La generación 19 del canal TEST incluye `lista-clinton` 0.1.3-candidate (`portal_id=5`, `document_id=33`). La verificación de transporte recuperó el PDF público de Treasury (16,539,778 bytes) y confirmó `%PDF-`; se validaron el paquete, firma y hashes. No se buscó ningún sujeto: el plan ORDS GET-only no tenía pares elegibles, por lo que no hay evidencia de documento ni ACK del robot.
