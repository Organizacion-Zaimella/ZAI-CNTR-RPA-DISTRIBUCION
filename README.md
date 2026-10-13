# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Candidato C.155 de TEST:** generación 77, motor `1.0.10-test.1`, Ministerio del Interior `0.1.4-candidate` y Fiscalía `0.1.8-candidate`; Superintendencia conserva su versión anterior por indisponibilidad del portal durante esta validación. Véase [estado y límites de las pruebas C.155](docs/C155_TEST_CANDIDATES.md). El canal productivo no cambia con este candidato.

**Canal TEST de `main` al abrir C.155:** generación 67 firmada, motor `1.0.7-test.1` y doce adaptadores publicados. El motor conserva el reintento visible acotado para fallos ocultos `PORTAL_UNAVAILABLE` o `ACTION_TIMEOUT` y procesa configuraciones mixtas. ORDS asigna solo los adaptadores requeridos por cada plan.

**Continuidad C.145:** este repositorio distribuye artefactos; ORDS decide qué asociación adaptador/función recibe cada trabajo. Los candidatos TEST requieren sus gates propios y no son autorización de Producción. Para continuar, verificar firma de `channels/test.json`, PR/rama/SHA y el expediente [C.145](https://github.com/Organizacion-Zaimella/ZAI-PRJ-CTRL-CAPTURA-INFORMACION-PUBLICA/tree/codex/c145-cierre-rpa-portales/docs/tareas/C.145). OpenClaw, workflows y Discovery son legado y no intervienen en la distribución ni ejecución 1.0.0.

INTERPOL 0.1.1 es un candidato técnico basado en workflow histórico 61/v2. Solo está probado con fixtures locales/sidecar; las URLs externas están bloqueadas por la política de autorización. No existe consulta real ni ACK ORDS para INTERPOL. La versión `lista-clinton@0.1.4-candidate` también permanece sujeta al estado y asignación que muestra el plan ORDS; la presencia en este canal no certifica por sí sola su ejecución integral.

**Canal PRODUCCION vigente al abrir C.155:** generación 8 firmada con motor `1.0.7` y las asignaciones publicadas. ORDS conserva el plan, orden y función; el canal firmado decide la versión ejecutable del adaptador compatible. Una referencia de versión atrasada en ORDS no detiene todos los documentos. El motor aísla fallos por lote y deja constancia en el detalle. INTERPOL permanece excluido.

Releases publicados en Producción: [motor 1.0.7](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.7) y [adaptador SRI 0.1.23](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.23).

La presencia de una versión en el canal permite su descarga firmada; la certificación documental requiere resultado, evidencia y ACK por trabajo real de ORDS.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Preparación de promoción C.151](docs/C151_PREPARACION_PRODUCCION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Canal PRODUCCION firmado](channels/production.json)
- [Contrato de versión, disponibilidad de assets y continuidad](docs/C153_VERSION_Y_CONTINUIDAD.md)
- [C.154 motor 1.0.6 TEST: reintento visible](docs/C154_ENGINE_1.0.6_VISIBLE_RETRY_TEST.md)
- [C.154 motor 1.0.7 TEST: configuraciones mixtas](docs/C154_ENGINE_1.0.7_CONFIGURACIONES_MIXTAS_TEST.md)
- [C.154 motor 1.0.7 Producción: configuraciones mixtas](docs/C154_ENGINE_1.0.7_PRODUCCION.md)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Los assets se publican en Releases y se autentican mediante firmas de canal separadas para TEST y Producción.
