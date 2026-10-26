# C.197 — Supercias 0.1.19 en Producción

El adaptador `supercias@0.1.19` se promovió desde `supercias@0.1.19-candidate`, probado en el canal TEST generación 114. La validación funcional real en Oracle TEST fue la ejecución 1966: una compañía existente completó tres documentos; el RUC inexistente produjo `SIN_RESULTADO` en tres documentos con evidencia y ACK para los seis detalles. El informe QA está en el repositorio documental, `qa/tareas/C.197/qa_test_supercias_ruc_inexistente.md`.

| Elemento | Valor |
|---|---|
| Fuente RPA | `f6e9e10c1f517e7d5c8ae03507fe3d5af653a2a1` |
| PR RPA integrado | [#72](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/pull/72), merge `0c6fd170a0bf1279326ebcf35f1fdae24f0f5b21` |
| Release TEST | [`cntr-rpa-supercias-0.1.19-test1`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.19-test1) |
| Release estable | [`cntr-rpa-supercias-0.1.19`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.19) |
| SHA-256 del paquete de Producción | `ab1bb74ca5345c0c18447fcc3729ff3abacda4b0024bf9d20c6aad0e8bfd8d73` |
| SHA-256 del manifiesto | `26b15d9f63dc396a39c1b3b87625ab48327ff2ba9685672cfce003c91702d4b3` |
| SHA-256 del SBOM | `807d80b7961169a46b44ce53bd5c8185c9ec4b9397a4375471715bf35e7ebd37` |

El asset estable se descargó anónimamente por HTTPS; HTTP 200 y tamaño/hash coincidieron con el canal firmado. La firma del asset, manifiesto y canal se verificó con la raíz Ed25519 de Producción.

## Canal productivo

El PR de distribución C.197 sube la generación de Producción de 29 a 30 y reemplaza únicamente `supercias@0.1.18` por `supercias@0.1.19`. Conserva el motor `1.0.27`, el resto de adaptadores y la lista de revocación. SHA-256 de `channels/production.json`: `1dea983ed4eaf72b8a6f4d0e4faa7da7b37955cb935ed393321ccb51d60ae7a1`. No requiere reinstalar el motor: el launcher instalado descarga el adaptador firmado al iniciar.
