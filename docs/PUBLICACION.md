# Política de publicación

## Superintendencia 0.1.8 — candidato TEST

Release firmado `cntr-rpa-supercias-0.1.8-test55` desde la fuente RPA
`1bfc366c7a2540558737b83c67982f3e2e276357`. El documento 16 sigue los pasos
vigentes de la ficha hacia **Administradores actuales**, selecciona la primera
fila con valor exacto `RL` y reutiliza la captura/validación PDF existente.
El fixture local Playwright y la regresión local del adaptador pasan. La
ejecución integrada robot/ORDS con este candidato queda pendiente; esta versión
no certifica el documento ni modifica Producción.

**Estado de canales:** el canal TEST generación 60 está en la rama candidata C.151 `codex/c151-supercias-test37`; el canal PROD generación 2 permanece sin cambios. El usuario amplió el alcance C.151 para solicitar un pase productivo, que sigue pendiente de pruebas reales y QA aprobado; un candidato TEST no equivale a certificación.

1. Desarrollar y revisar el cambio en su repositorio privado, con commit exacto y pruebas de contrato.
2. Verificar que el contenido público no incluya datos personales, evidencias, cookies, tokens, URLs internas ni claves privadas. Confirmar derechos de publicación antes de copiar un adaptador.
3. Construir desde fuente aprobada con dependencias bloqueadas, registrar SBOM, compatibilidad y SHA-256; firmar manifest y artefactos mediante una clave custodiada fuera de este repositorio.
4. Publicar assets en un GitHub Release inmutable, sin sobrescribir tags ni assets existentes. Un build no equivale a release aprobada.
5. Promover canal TEST y luego Producción mediante PR revisado y checks definidos. El puntero firmado se actualiza solo después de que el asset existe y pasa los gates del canal.
6. Documentar revocación y reversión. Una versión retirada no debe ejecutarse por estar en caché.

El canal TEST generación 60 y sus Releases están en la rama candidata C.151. El canal PROD firmado generación 2 conserva su estado independiente; cada promoción TEST se comprueba con firma, hash y preflight antes de habilitarla para pruebas. Servicios Educación, SENESCYT y Superintendencia 0.1.11 son candidatos no certificados, a la espera de prueba atendida, ejecución integrada y ACK. Los adaptadores educativos ya están asignados en Oracle TEST; no se ejecutaron consultas de portal.

## Lista Clinton 0.1.4 — candidato TEST

La fuente RPA `1f24b164aa7f46ec463bbe459f3d3c8a5091e7b1` genera el paquete
firmado `lista_clinton@0.1.4-candidate` en la generación TEST 21. El cambio
limita a 30 los números de página en la salida JSON, conserva el total e indica
truncamiento. La suite local obtuvo 15 resultados aprobados y una comprobación
local sobre un PDF público completo de 3.232 páginas validó el bundle. Esa
comprobación no usó sujeto CNTR ni produjo ejecución/ACK. ORDS TEST aún no asigna
función ni pareja elegible al documento 33; esta publicación es candidata y no
autoriza su ejecución desde ORDS ni Producción.
