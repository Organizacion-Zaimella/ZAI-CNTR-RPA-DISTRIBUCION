# C.151-ST07 — ritmo de interacción de documentos educativos

Fecha: 2026-11-17. Estado: candidatos firmados para integración y QA en TEST; no promovidos a Producción.

| Componente | Versión | Release TEST | Función | Fuente RPA |
|---|---|---|---|---|
| Motor | `1.0.30-test.1` | `cntr-rpa-engine-1.0.30-test1` | allowlist de pausas | `418ad1f7ea95f420c83a16e088cc5a97ac4d7cb6` |
| Servicios Educación | `0.1.4-candidate` | `cntr-rpa-servicios-educacion-0.1.4-test1` | `documento_9` | `418ad1f7ea95f420c83a16e088cc5a97ac4d7cb6` |
| SENESCYT | `0.1.7-candidate` | `cntr-rpa-senescyt-0.1.7-test1` | `documento_10` | `418ad1f7ea95f420c83a16e088cc5a97ac4d7cb6` |

El canal TEST candidato es la generación `133`; el canal de Producción sigue intacto. La pausa de 2 segundos aplica únicamente a portal 9/documento 9/adaptador `servicios_educacion` y portal 10/documento 10/adaptador `senescyt`. Todos los demás documentos conservan el mínimo de 5 segundos. La espera de CAPTCHA/operador, estabilización y resultado no cambia.

Validación local: 110 pruebas aprobadas y 4 omitidas entre el motor y las dos aplicaciones. El build del motor pasó 88 pruebas, 4 omitidas, el preflight de navegador y ejecución congelada del adaptador en sidecar.

La corrida 2108 quedó interrumpida después de dos pares de doc. 9; la ejecución original no probó doc. 10 y no certifica estos candidatos. El QA integrado pendiente usará una configuración aislada con los mismos tres sujetos de la ejecución productiva 2602, exclusivamente documentos 9 y 10: seis pares, evidencia y ACK. Los datos de sujetos y evidencias permanecen privados. No se realizó ningún cambio en Producción.
