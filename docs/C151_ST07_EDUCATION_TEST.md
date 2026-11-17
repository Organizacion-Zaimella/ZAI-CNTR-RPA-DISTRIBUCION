# C.151-ST07 — ritmo de interacción de documentos educativos

Fecha: 2026-11-17. Estado: QA aprobada en TEST; canal candidato firmado generación 133. Promoción a Producción pendiente.

| Componente | Versión | Release TEST | Función | Fuente RPA |
|---|---|---|---|---|
| Motor | `1.0.30-test.1` | `cntr-rpa-engine-1.0.30-test1` | allowlist de pausas | `418ad1f7ea95f420c83a16e088cc5a97ac4d7cb6` |
| Servicios Educación | `0.1.4-candidate` | `cntr-rpa-servicios-educacion-0.1.4-test1` | `documento_9` | `418ad1f7ea95f420c83a16e088cc5a97ac4d7cb6` |
| SENESCYT | `0.1.7-candidate` | `cntr-rpa-senescyt-0.1.7-test1` | `documento_10` | `418ad1f7ea95f420c83a16e088cc5a97ac4d7cb6` |

El canal TEST candidato es la generación `133`; el canal de Producción sigue intacto. La pausa de 2 segundos aplica únicamente a portal 9/documento 9/adaptador `servicios_educacion` y portal 10/documento 10/adaptador `senescyt`. Todos los demás documentos conservan el mínimo de 5 segundos. La espera de CAPTCHA/operador, estabilización y resultado no cambia.

Validación local: 110 pruebas aprobadas y 4 omitidas entre el motor y las dos aplicaciones. El build del motor pasó 88 pruebas, 4 omitidas, el preflight de navegador y ejecución congelada del adaptador en sidecar. El gate público anónimo verificó los 13 componentes del canal TEST: manifiestos, firmas, SBOM y ZIP correctos; estado `PASS` para generación 133.

## Resultado de QA integrado

La corrida controlada en Oracle TEST procesó los documentos 9 y 10 y recibió cuatro trabajos elegibles: uno de Servicios Educación y tres de SENESCYT. Los cuatro terminaron con evidencia y ACK `ACKED`, incluidos los resultados `SIN_RESULTADO`. Se confirmó que el documento 10 con el caso previamente reportado también capturó evidencia. La corrida anterior 2108 queda como antecedente incompleto y no se usa como resultado de esta validación.

El cambio de 2 segundos se limita a portal/documento 9/9 y 10/10; el resto del canal y de los tiempos permanece sin cambios. Los datos de sujetos y evidencias se conservan fuera de este repositorio. Este registro de QA TEST no cambia el canal ni los pins de Producción.
