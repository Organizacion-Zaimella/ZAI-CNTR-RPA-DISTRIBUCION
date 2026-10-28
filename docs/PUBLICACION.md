# Política de publicación

**Candidato C.153:** TEST generación 65 conserva el candidato SRI `0.1.23-candidate`, probado en documentos 3/53 con evidencias y ACK. La Producción propuesta es generación 6, motor `1.0.4` y SRI `0.1.23`; conserva las demás asignaciones de la generación 4, revoca `engine@1.0.3` y `adapter:sri@0.1.22`, y mantiene INTERPOL fuera. El motor 1.0.4 se compiló desde el commit RPA `a2dc3aaf796aeb32c90f08c1e9e104cf16ac084e`; 49 pruebas del motor aprobaron, 2 se omitieron y el build validó versión, preflight Edge/Chrome y ejecución sidecar. La corrección genérica recibió cuatro pruebas enfocadas aprobadas y 20 pruebas del updater aprobaron. No se inició una ejecución documental en Producción.

1. Desarrollar y revisar el cambio en su repositorio privado, con commit exacto y pruebas de contrato.
2. Verificar que el contenido público no incluya datos personales, evidencias, cookies, tokens, URLs internas ni claves privadas. Confirmar derechos de publicación antes de copiar un adaptador.
3. Construir desde fuente aprobada con dependencias bloqueadas, registrar SBOM, compatibilidad y SHA-256; firmar manifest y artefactos mediante una clave custodiada fuera de este repositorio.
4. Publicar assets en un GitHub Release inmutable, sin sobrescribir tags ni assets existentes. Un build no equivale a release aprobada.
5. Promover canal TEST y luego Producción mediante PR revisado y checks definidos. El puntero firmado se actualiza solo después de que el asset existe y pasa los gates del canal.
6. Documentar revocación y reversión. Una versión retirada no debe ejecutarse por estar en caché.

Los estados “sin release publicable” de T01 y generación 2 de C.145 son históricos. Los assets de motor 1.0.4 y SRI 0.1.23 están publicados con manifiestos firmados. Esta rama propone el puntero generación 6; hasta integrar este cambio en `main`, el launcher conserva el canal anterior. La verificación de firma/hash y la lectura JSON/firma desde un mismo SHA siguen siendo obligatorias.

## Lista Clinton 0.1.4 — candidato TEST

La fuente RPA `1f24b164aa7f46ec463bbe459f3d3c8a5091e7b1` genera el paquete
firmado `lista_clinton@0.1.4-candidate` en la generación TEST 21. El cambio
limita a 30 los números de página en la salida JSON, conserva el total e indica
truncamiento. La suite local obtuvo 15 resultados aprobados y una comprobación
local sobre un PDF público completo de 3.232 páginas validó el bundle. Esa
comprobación no usó sujeto CNTR ni produjo ejecución/ACK. ORDS TEST aún no asigna
función ni pareja elegible al documento 33; esta publicación es candidata y no
autoriza su ejecución desde ORDS ni Producción.

## C.180/C.181 — promoción de motor 1.0.25 y Ministerio del Interior 0.1.9

- En TEST se validaron el motor `1.0.25-test.1` y `ministerio_interior@0.1.9-candidate` en una ejecución ORDS real de dos sujetos. El CAPTCHA visible fue resuelto por el operador; los dos detalles terminaron `COMPLETADO`, guardaron evidencia y recibieron ACK. El navegador mantuvo una sola sesión para los dos trabajos.
- La verificación del motor conservó `strict=True` y filtró únicamente el aviso recuperable `Xref table not zero-indexed...`. QA PDF, suite V100, constructor, firma y actualizador aprobaron. La suite heredada completa dejó tres fallos no relacionados, registrados en el informe C.181.
- Antes de mover el puntero, se publicaron los Releases estables firmados `cntr-rpa-engine-1.0.25` y `cntr-rpa-ministerio_interior-0.1.9`. La descarga anónima de ZIP, manifiestos, firmas y SBOM se verificó contra hashes y trust root.
- El canal firmado PRODUCCIÓN generación 26 conserva las otras nueve asignaciones y las cuatro revocaciones de la generación 25; solo actualiza el motor y el adaptador Ministerio. El launcher instalado aplica la actualización al iniciar, sin reinstalación.
- El PR #61 se integró en `main` como `da14ef54d002a43e65a7cbfaece66d57c9b522bd`. La lectura pública del canal y su firma Ed25519 confirmaron generación 26, motor 1.0.25 y `ministerio_interior@0.1.9`; los assets públicos pasaron HTTP 200, hash y firma.
- Los launchers instalados pueden ejecutar ahora y descargar el motor/adaptador actualizados al iniciar; no hace falta reinstalarlos.
- Evidencias: `docs/C180_C181_PRODUCTION.md` y QA ORDS TEST `1927` en el expediente C.180. No se ejecutó QA documental en Producción.

## C.200 — verificación completa antes de promover

Antes de integrar cualquier canal TEST o PRODUCCIÓN, ejecutar en Windows desde el repositorio RPA la herramienta versionada `scripts/verify_public_channel.py` con el canal candidato y su firma. El informe debe indicar `GATE PASS` para el motor y todos los adaptadores del canal, incluidos los que permanecen sin cambios. Verifica descarga anónima, manifiestos y firmas, SBOM y ZIP según el contrato firmado. Registrar el SHA del candidato y el informe en el expediente. Si falla cualquier componente, corregirlo antes de promover.

Después de integrar, ejecutar nuevamente la herramienta sin archivos candidatos para verificar el canal público de `main` y conservar ese informe. La sintaxis completa está en `FLUJO_OPERATIVO_RPA.md` del repositorio RPA. La herramienta no configura automáticamente checks obligatorios en la protección de rama.
