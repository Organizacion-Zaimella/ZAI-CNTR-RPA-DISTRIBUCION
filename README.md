# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Canal TEST de esta rama:** generación 65 firmada, motor `1.0.2-test.1` y doce adaptadores publicados. ORDS asigna solo los necesarios para cada plan. C.152 verificó desde la instalación existente la actualización independiente de `sri@0.1.22-candidate` a `sri@0.1.23-candidate`, con evidencias y ACK para los documentos 3 y 53.

**Continuidad C.145:** este repositorio distribuye artefactos; ORDS decide qué asociación adaptador/función recibe cada trabajo. Los candidatos TEST requieren sus gates propios y no son autorización de Producción. Para continuar, verificar firma de `channels/test.json`, PR/rama/SHA y el expediente [C.145](https://github.com/Organizacion-Zaimella/ZAI-PRJ-CTRL-CAPTURA-INFORMACION-PUBLICA/tree/codex/c145-cierre-rpa-portales/docs/tareas/C.145). OpenClaw, workflows y Discovery son legado y no intervienen en la distribución ni ejecución 1.0.0.

INTERPOL 0.1.1 es un candidato técnico basado en workflow histórico 61/v2. Solo está probado con fixtures locales/sidecar; las URLs externas están bloqueadas por la política de autorización. No existe consulta real ni ACK ORDS para INTERPOL. La versión `lista-clinton@0.1.4-candidate` también permanece sujeta al estado y asignación que muestra el plan ORDS; la presencia en este canal no certifica por sí sola su ejecución integral.

**Canal PRODUCCION propuesto por C.152:** generación 4 firmada con motor `1.0.3` y los diez adaptadores de la generación 3 aprobada. El cambio de motor muestra progreso y resumen y clasifica los timeouts transitorios sin atribuirlos a caída del portal. INTERPOL permanece excluido.

La generación 3 de C.151 ya está integrada en `main`. El release productivo `1.0.2` preexistente tiene bytes distintos; C.152 publica `1.0.3` sin reutilizar ese nombre. La firma de `channels/production.json` y el asset `1.0.3` son el par de promoción de esta rama.

La presencia de una versión en el canal permite su descarga firmada; la certificación documental requiere resultado, evidencia y ACK por trabajo real de ORDS.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Preparación de promoción C.151](docs/C151_PREPARACION_PRODUCCION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Canal PRODUCCION firmado](channels/production.json)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Los assets se publican en Releases y se autentican mediante firmas de canal separadas para TEST y Producción.
