# C.199 — Supercias 0.1.20 en Producción

El adaptador `supercias@0.1.20` se promueve desde `supercias@0.1.20-candidate`, probado en TEST generación 115. La mejora del documento 19 busca el balance más reciente del año actual y el del año anterior, y guarda los PDF disponibles como una sola evidencia. Si el balance del año anterior no está disponible, conserva como evidencia el PDF del año actual.

| Elemento | Valor |
|---|---|
| Fuente RPA | `65ab74bc7b252c031785cdab89dec4d1c48c0103` |
| PR RPA integrado | [#73](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/pull/73) |
| QA TEST | Ejecución 2008 / detalle 2722; `COMPLETADO`, ACK `ACKED`; PDF de 16 páginas con los ejercicios 2025 y 2024 |
| Release TEST | [`cntr-rpa-supercias-0.1.20-test1`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.20-test1) |
| Release estable | [`cntr-rpa-supercias-0.1.20`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.20) |
| SHA-256 del paquete de Producción | `b1973c9a7273e2354f93a709884e7b97dcb90930358a36fc1d76777aaa8dd274` |
| SHA-256 del manifiesto | `c61e0cc1575ce2daff6a8de6641ecdd4dd42ecc002cb37b81f543dfa51ed75c1` |
| SHA-256 del SBOM | `c1992670d79dfcf3cb65da1ec4008fa7a6854791dbecccb4f65c8b4d32109be2` |
| Generación de Producción | `31`; SHA-256 de `channels/production.json`: `c06708d8cb355ef2c3250d3221d9098616ffce9125344eaaa05db3d84bebd4c4` |
| Firma | Raíz Ed25519 de Producción `cntr-prod-63f2371d344a` |

El paquete estable se creó a partir del asset del candidato público; se validaron su hash, firma y manifiesto. La descarga pública anónima del release estable respondió HTTP 200 y coincidió con tamaño y SHA-256. El canal firmado cambia solo Supercias; el motor, los demás adaptadores y la lista de revocación permanecen iguales a generación 30. Los usuarios con el launcher instalado reciben el adaptador al iniciar el robot; no requieren reinstalarlo.
