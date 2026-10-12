# Arquitectura de distribución

**Estado candidato C.151:** la infraestructura no está en estado inicial. La rama candidata `codex/c151-supercias-test37` publica el canal TEST firmado generación 51; el inventario y SHA están en [VERSIONES_TEST](../channels/VERSIONES_TEST.md). El canal de Producción generación 2 permanece separado y sin cambios en este trabajo. Confirmar rama/SHA y firma antes de usar. El motor es genérico Python + Playwright; OpenClaw/workflows son legado.

## Responsabilidades

El desarrollo del motor y adaptadores se conserva en el repositorio de trabajo privado `Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA`. Oracle/ORDS conserva reglas, catálogo, sujetos, elegibilidad, orden, sesiones, estado y auditoría. Este repositorio público contendrá únicamente documentación publicable y, tras certificación, código depurado de adaptadores, manifiestos firmados y assets de GitHub Releases.

El launcher estable consultará un canal fijado localmente, validará firma, procedencia, digest, compatibilidad y revocación antes de instalar motor o adaptadores. El motor ejecutará el plan recibido de ORDS; un manifest público no decide qué sujeto o documento corresponde procesar.

## Separación de versiones

El motor 1.0.0 y cada adaptador tendrán versiones independientes. El contrato de adaptadores y el formato de manifest se definen en `contracts/`. Los binarios y ZIP certificados se alojarán como assets de Releases; Git no contendrá ejecutables.


## Límites de certificación

La inclusión de un adaptador en el canal indica que el paquete puede descargarse y verificarse dentro de su ambiente; no acredita por sí sola ejecución real de portal, evidencia/ACK ni habilitación productiva. INTERPOL 0.1.1 permanece limitado a fixtures loopback y sin consulta real/ACK. Ningún dato de sujetos, credenciales ni evidencia real se publica aquí.
