# Arquitectura de distribución

## Responsabilidades

El desarrollo del motor y adaptadores se conserva en el repositorio privado `Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA`. Oracle/ORDS conserva catálogo, sujetos, elegibilidad, orden, sesiones, estado y auditoría. Este repositorio público sirve documentación, contratos, punteros firmados de canal y assets versionados de GitHub Releases.

El launcher estable verifica procedencia, firma, digest, compatibilidad y revocación antes de instalar motor o adaptadores. El motor procesa el plan recibido de ORDS; un manifiesto público nunca decide qué sujeto o documento se ejecuta.

## Separación de versiones

El motor 1.0.0 y cada adaptador tienen versiones independientes. Los contratos de adaptador y manifiestos están en `contracts/`. Los paquetes descargables se publican como assets de Releases; Git no guarda ejecutables.

## Estado por canal

- `main`: documentación estable. No apunta a candidatos TEST.
- `codex/c144-sri-test`: rama de pruebas con canal TEST firmado durante C.144. El candidato SRI 0.1.13 soporta documentos 3 y 53 y se valida únicamente en TEST.
- Producción: no hay canal ni publicación productiva en este expediente.
