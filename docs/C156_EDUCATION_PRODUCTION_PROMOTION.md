# C.156 — promoción productiva de títulos educativos

Alcance: únicamente `servicios_educacion` documento 9 y `senescyt`
documento 10. El motor `1.0.10` y los demás adaptadores conservan exactamente
los valores del canal de Producción generación 9. INTERPOL permanece fuera.

| Adaptador | TEST certificado | Producción anterior | Producción generación 10 |
|---|---|---|---|
| Servicios Educación | `0.1.2-candidate` | `0.1.0-candidate` | [`0.1.2`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-servicios_educacion-0.1.2) |
| SENESCYT | `0.1.3-candidate` | `0.1.0-candidate` | [`0.1.3`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-senescyt-0.1.3) |

Fuente RPA: [PR #38](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/pull/38).
La integración instalada TEST se documenta en
[`C156_TITULOS_INTEGRACION_TEST_20261014.md`](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/blob/main/docs/v1.0.0/tareas/C156_TITULOS_INTEGRACION_TEST_20261014.md):
dos sujetos por documento, cuatro resultados finales con evidencia y ACK.
Los nombres, identificaciones y capturas permanecen fuera del repositorio.

Los ZIP productivos derivan de los ZIP firmados del canal TEST generación 87:
se conserva el Python y solo se cambia `adapter-manifest.json` de
`TEST_CANDIDATE` a `PRODUCTION`, con versión estable. Se verificaron firma,
inventario, tamaño y SHA-256 localmente. Descargas públicas anónimas de los
dos Releases productivos respondieron HTTP 200 y reprodujeron los hashes del
canal firmado:

- Servicios Educación: `2053693efd7e57385067bcae20bfed0d58b8f7d6c7a2bf2ac7da1efe2cf8ba90`.
- SENESCYT: `128b9887e92dbb1178f214c57cf2f97f9237354bfe22adbf36463cbbc632203d`.
- `channels/production.json` generación 10: `ad230b0a029eecfbcc1d1765c86245fe3bd6a29712ec7926319787cdfeddb997`.

El SQL productivo versionado en el PR #38 exige los dos valores anteriores y
actualiza solo `DATA.T_CNTR_DOCUMENTOS.ID_DOCUMENTO IN (9,10)`; no crea sujetos,
documentos ni ejecuciones. Tras publicar este canal, aplicar ese SQL por el
ejecutor oficial. La reversión conserva los Releases y requiere primero un
nuevo canal firmado que recupere los dos adaptadores anteriores; después se
puede ejecutar el SQL de rollback del PR #38. No reutilizar la generación 9
como un número nuevo ni revocar los artefactos previos antes de terminar el
pase.
