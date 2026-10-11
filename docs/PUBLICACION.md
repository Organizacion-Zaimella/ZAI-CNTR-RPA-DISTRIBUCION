# Política de publicación

**Estado C.145:** TEST generación 36 está disponible en su rama candidata. El canal PROD generación 2 está firmado con motor 1.0.1 y cinco adaptadores para los diez documentos exitosos; INTERPOL queda excluido. El motor 1.0.0 está revocado para evitar retroceder a una versión que no ejecutaba Producción. La autorización del usuario para el pase y el instalador está registrada en el expediente C.145.

1. Desarrollar y revisar el cambio en su repositorio privado, con commit exacto y pruebas de contrato.
2. Verificar que el contenido público no incluya datos personales, evidencias, cookies, tokens, URLs internas ni claves privadas. Confirmar derechos de publicación antes de copiar un adaptador.
3. Construir desde fuente aprobada con dependencias bloqueadas, registrar SBOM, compatibilidad y SHA-256; firmar manifest y artefactos mediante una clave custodiada fuera de este repositorio.
4. Publicar assets en un GitHub Release inmutable, sin sobrescribir tags ni assets existentes. Un build no equivale a release aprobada.
5. Promover canal TEST y luego Producción mediante PR revisado y checks definidos. El puntero firmado se actualiza solo después de que el asset existe y pasa los gates del canal.
6. Documentar revocación y reversión. Una versión retirada no debe ejecutarse por estar en caché.

El canal TEST generación 36 y sus Releases están en la rama candidata C.145. El estado “sin release publicable” de T01 es histórico y no representa la rama candidata actual. El canal PROD firmado generación 2 contiene motor 1.0.1 y los cinco adaptadores requeridos por los diez documentos probados; no incluye INTERPOL. Cada promoción se comprueba con descarga pública, firma, hash y preflight antes de entregar el instalador.

## Lista Clinton 0.1.4 — candidato TEST

La fuente RPA `1f24b164aa7f46ec463bbe459f3d3c8a5091e7b1` genera el paquete
firmado `lista_clinton@0.1.4-candidate` en la generación TEST 21. El cambio
limita a 30 los números de página en la salida JSON, conserva el total e indica
truncamiento. La suite local obtuvo 15 resultados aprobados y una comprobación
local sobre un PDF público completo de 3.232 páginas validó el bundle. Esa
comprobación no usó sujeto CNTR ni produjo ejecución/ACK. ORDS TEST aún no asigna
función ni pareja elegible al documento 33; esta publicación es candidata y no
autoriza su ejecución desde ORDS ni Producción.
