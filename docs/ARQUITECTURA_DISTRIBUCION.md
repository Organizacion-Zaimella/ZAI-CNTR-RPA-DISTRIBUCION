# Arquitectura de distribución

## Responsabilidades

El desarrollo del motor y adaptadores se conserva en el repositorio de trabajo privado `Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA`. Oracle/ORDS conserva reglas, catálogo, sujetos, elegibilidad, orden, sesiones, estado y auditoría. Este repositorio público contendrá únicamente documentación publicable y, tras certificación, código depurado de adaptadores, manifiestos firmados y assets de GitHub Releases.

El launcher estable consultará un canal fijado localmente, validará firma, procedencia, digest, compatibilidad y revocación antes de instalar motor o adaptadores. El motor ejecutará el plan recibido de ORDS; un manifest público no decide qué sujeto o documento corresponde procesar.

## Separación de versiones

El motor 1.0.0 y cada adaptador tendrán versiones independientes. El contrato de adaptadores y el formato de manifest se definen en `contracts/`. Los binarios y ZIP certificados se alojarán como assets de Releases; Git no contendrá ejecutables.

## Estado inicial

En `main` no existen canales ni releases. La rama de tarea T07 mantiene un canal `TEST` firmado de generación 3 y un prerelease candidato para validar la descarga anónima; no hay canal de Producción ni releases certificados. No se publican sujetos, evidencias, secretos ni endpoints internos.
