# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Canal TEST de `main`:** generación 65 firmada, motor `1.0.2-test.1` y doce adaptadores publicados. La rama candidata C.154 `codex/c154-visible-retry` propone generación 66 con motor `1.0.6-test.1`, manteniendo las doce asignaciones. El cambio reintenta una sola vez en primer plano un trabajo automático que falló oculto por `PORTAL_UNAVAILABLE` o `ACTION_TIMEOUT`; no cambia Producción ni certifica documentos por sí solo. ORDS asigna solo los adaptadores requeridos por cada plan.

**Continuidad C.145:** este repositorio distribuye artefactos; ORDS decide qué asociación adaptador/función recibe cada trabajo. Los candidatos TEST requieren sus gates propios y no son autorización de Producción. Para continuar, verificar firma de `channels/test.json`, PR/rama/SHA y el expediente [C.145](https://github.com/Organizacion-Zaimella/ZAI-PRJ-CTRL-CAPTURA-INFORMACION-PUBLICA/tree/codex/c145-cierre-rpa-portales/docs/tareas/C.145). OpenClaw, workflows y Discovery son legado y no intervienen en la distribución ni ejecución 1.0.0.

INTERPOL 0.1.1 es un candidato técnico basado en workflow histórico 61/v2. Solo está probado con fixtures locales/sidecar; las URLs externas están bloqueadas por la política de autorización. No existe consulta real ni ACK ORDS para INTERPOL. La versión `lista-clinton@0.1.4-candidate` también permanece sujeta al estado y asignación que muestra el plan ORDS; la presencia en este canal no certifica por sí sola su ejecución integral.

**Canal PRODUCCION vigente:** generación 6 firmada con motor `1.0.4` y SRI `0.1.23`. **Candidato C.153 de estabilidad:** generación 7 firmada con motor `1.0.5` y las mismas diez versiones de adaptadores. ORDS conserva el plan, orden y función; el canal firmado decide la versión ejecutable del adaptador compatible. Una referencia de versión atrasada en ORDS no detiene todos los documentos. El motor aísla fallos por lote y deja constancia en el detalle. INTERPOL permanece excluido. La generación 7 se activa únicamente al integrar este PR.

Releases publicados: [motor 1.0.5](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.5) y [adaptador SRI 0.1.23](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.23). La generación 7 se mantiene en el PR hasta su integración.

La presencia de una versión en el canal permite su descarga firmada; la certificación documental requiere resultado, evidencia y ACK por trabajo real de ORDS.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Preparación de promoción C.151](docs/C151_PREPARACION_PRODUCCION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Canal PRODUCCION firmado](channels/production.json)
- [Contrato de versión, disponibilidad de assets y continuidad](docs/C153_VERSION_Y_CONTINUIDAD.md)
- [C.154 motor 1.0.6 TEST: reintento visible](docs/C154_ENGINE_1.0.6_VISIBLE_RETRY_TEST.md)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Los assets se publican en Releases y se autentican mediante firmas de canal separadas para TEST y Producción.
