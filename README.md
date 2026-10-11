# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Canal TEST de esta rama:** generación 36 firmada. El manifiesto es la referencia de versiones para esta integración: motor `1.0.0-test.13` y ocho adaptadores TEST. [Inventario exacto](channels/VERSIONES_TEST.md).

**Continuidad C.145:** este repositorio distribuye artefactos; ORDS decide qué asociación adaptador/función recibe cada trabajo. Los candidatos TEST requieren sus gates propios y no son autorización de Producción. Para continuar, verificar firma de `channels/test.json`, PR/rama/SHA y el expediente [C.145](https://github.com/Organizacion-Zaimella/ZAI-PRJ-CTRL-CAPTURA-INFORMACION-PUBLICA/tree/codex/c145-cierre-rpa-portales/docs/tareas/C.145). OpenClaw, workflows y Discovery son legado y no intervienen en la distribución ni ejecución 1.0.0.

INTERPOL 0.1.1 es un candidato técnico basado en workflow histórico 61/v2. Solo está probado con fixtures locales/sidecar; las URLs externas están bloqueadas por la política de autorización. No existe consulta real ni ACK ORDS para INTERPOL. La versión `lista-clinton@0.1.4-candidate` también permanece sujeta al estado y asignación que muestra el plan ORDS; la presencia en este canal no certifica por sí sola su ejecución integral.

La presencia de una versión en el canal permite su descarga firmada; la certificación documental requiere resultado, evidencia y ACK por trabajo real de ORDS.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Todo asset es un candidato de TEST, no una autorización para Producción.
