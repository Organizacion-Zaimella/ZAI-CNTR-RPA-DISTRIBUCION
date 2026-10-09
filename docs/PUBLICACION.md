# Política de publicación

1. Desarrollar y revisar el cambio en su repositorio privado, con commit exacto y pruebas de contrato.
2. Verificar que el contenido público no incluya datos personales, evidencias, cookies, tokens, URLs internas ni claves privadas. Confirmar derechos de publicación antes de copiar un adaptador.
3. Construir desde fuente aprobada con dependencias bloqueadas, registrar SBOM, compatibilidad y SHA-256; firmar manifest y artefactos mediante una clave custodiada fuera de este repositorio.
4. Publicar assets en un GitHub Release inmutable, sin sobrescribir tags ni assets existentes. Un build no equivale a release aprobada.
5. Promover canal TEST y luego Producción mediante PR revisado y checks definidos. El puntero firmado se actualiza solo después de que el asset existe y pasa los gates del canal.
6. Documentar revocación y reversión. Una versión retirada no debe ejecutarse por estar en caché.

La rama `main` alberga la documentación base. La rama draft de T07 incorpora un canal TEST de generación 3 y el prerelease candidato `cntr-rpa-1.0.0-test.3`; ambos se usan para QA anónimo de motor y adaptadores. La actualización incluye una corrección del transporte del origen canónico al crear detalles ORDS. Esto no certifica funcionalidad ni aprueba Producción. El control de branch y aprobadores se comprueba por separado; este documento no afirma que estén configurados.
