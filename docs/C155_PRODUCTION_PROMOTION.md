# C.155 — promoción productiva firmada

Este PR propone **canal de Producción generación 9**; la generación 8 permanece activa hasta integrar el PR. La fuente RPA de C.155 se integró en [PR #35](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/pull/35) y Oracle/ORDS en [PR #18](https://github.com/Organizacion-Zaimella/zaimella-apex-oracle/pull/18). La revisión TEST con IDs, evidencia y ACK saneados está en el [expediente C.155](https://github.com/Organizacion-Zaimella/ZAI-PRJ-CTRL-CAPTURA-INFORMACION-PUBLICA/pull/7).

| Componente | Antes | Propuesto | Release firmado |
|---|---|---|---|
| Motor | 1.0.7 | 1.0.10 | [motor](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.10) |
| Fiscalía | 0.1.4-candidate | 0.1.9 | [adaptador](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-fiscalia-0.1.9) |
| Ministerio del Interior | 0.1.1-candidate | 0.1.6 | [adaptador](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ministerio_interior-0.1.6) |
| Superintendencia | 0.1.14-candidate | 0.1.16 | [adaptador](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.16) |

Los otros siete adaptadores permanecen idénticos a la generación 8; INTERPOL continúa fuera del canal. La promoción convierte únicamente `adapter-manifest.json` de `TEST_CANDIDATE` a `PRODUCTION` y asigna las versiones estables; los bytes de aplicación de cada adaptador proceden de los ZIP firmados de TEST generación 82. El motor 1.0.10 se construyó desde la fuente de runtime `c858f3d4ece9d9d1146d82a26c319fbba032c805` sin cambios posteriores en `src/cntr_rpa_v100`, `run_v100.py` o dependencias. Build: preflight y sidecar externo correctos.

La clave de Producción protegida por DPAPI firmó por separado cada asset, manifiesto y el canal. La verificación local de firma, inventario y SHA-256 aprobó. Una sesión HTTP anónima (`trust_env=False`, sin encabezado `Authorization`) descargó los cuatro ZIP desde GitHub con **HTTP 200**, tamaño y SHA-256 iguales al canal firmado. SHA-256 de `channels/production.json`: `39a0298468c47b44277b064e7807da3b05c0a356adbd394e62eb18a0b35d3fb4`.

El pase Oracle productivo debe alinear `ADAPTADOR_FUNCION` de los documentos 4, 8 y 16 con las versiones estables, y desplegar `PK_CNTR_ORDS` rc.7 desde el SHA integrado en `main`. El puntero no debe activarse antes de que los Releases y la asignación Oracle estén preparados. La generación 8 y sus assets se conservan para reversión; no se revocan aquí. No se incluyen datos de sujetos, credenciales ni evidencias documentales.
