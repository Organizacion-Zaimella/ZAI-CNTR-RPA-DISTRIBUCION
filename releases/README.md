# Releases

Los ejecutables, ZIP y paquetes certificados se distribuyen exclusivamente como assets de GitHub Releases, junto con manifiesto firmado, digests, compatibilidad, procedencia y SBOM.

## Candidato TEST de motor

- Tag: `cntr-rpa-engine-1.0.0-test.1` (prerelease TEST; no es una versión estable ni de Producción).
- Contenido: motor Windows x64 1.0.0 únicamente; no incluye adaptadores ni datos de sujetos.
- Fuente: commit RPA `17325a6a88f897a657ce97b687f140e61f13aec6`.
- Estado del canal: se propone en PR de rama para prueba anónima del launcher; `main`/Producción no se modifica.

## Candidato TEST de OFAC

- Tag: `cntr-rpa-ofac-0.1.4-test1` (prerelease TEST; no es aprobación de Producción).
- Contenido: adaptador OFAC documento 5, app Playwright independiente, manifiesto, firma y SBOM.
- Fuente: commit RPA `8b164b110bdbe4eadb1a0a4e687feca0143114c1`.
- Validación: Gate A independiente registrado en el PR del adaptador; canal TEST generación 18. El plan ORDS actual no contiene una pareja OFAC elegible, por lo que no se afirma ejecución instalada ni ACK.
- Estado: candidato; promoción y certificación quedan pendientes de una pareja legítimamente elegible y su ejecución integrada.

Esta carpeta contiene documentación. Los assets binarios están en GitHub Releases.
