# CNTR RPA — distribución pública

Repositorio público de distribución de software aprobado del proyecto CNTR RPA. El canal TEST permite validar paquetes firmados y compatibles; su presencia no certifica la captura integral de un documento ni habilita Producción.

**Canal TEST de esta rama:** generación 65 firmada, motor `1.0.2-test.1` y doce adaptadores publicados. ORDS asigna solo los necesarios para cada plan. C.152 verificó desde la instalación existente la actualización independiente de `sri@0.1.22-candidate` a `sri@0.1.23-candidate`, con evidencias y ACK para los documentos 3 y 53.

**Continuidad C.145:** este repositorio distribuye artefactos; ORDS decide qué asociación adaptador/función recibe cada trabajo. Los candidatos TEST requieren sus gates propios y no son autorización de Producción. Para continuar, verificar firma de `channels/test.json`, PR/rama/SHA y el expediente [C.145](https://github.com/Organizacion-Zaimella/ZAI-PRJ-CTRL-CAPTURA-INFORMACION-PUBLICA/tree/codex/c145-cierre-rpa-portales/docs/tareas/C.145). OpenClaw, workflows y Discovery son legado y no intervienen en la distribución ni ejecución 1.0.0.

INTERPOL 0.1.1 es un candidato técnico basado en workflow histórico 61/v2. Solo está probado con fixtures locales/sidecar; las URLs externas están bloqueadas por la política de autorización. No existe consulta real ni ACK ORDS para INTERPOL. La versión `lista-clinton@0.1.4-candidate` también permanece sujeta al estado y asignación que muestra el plan ORDS; la presencia en este canal no certifica por sí sola su ejecución integral.

**Candidato de canal PRODUCCION C.153:** generación 6 firmada con motor `1.0.4` y SRI `0.1.23`; conserva las demás asignaciones de la generación 4 y revoca `engine@1.0.3` y `adapter:sri@0.1.22`. El motor aísla fallos del adaptador y continúa el plan en el orden ORDS. SRI 0.1.23 proviene del candidato TEST 0.1.23-candidate, probado con documentos 3/53, evidencias y ACK en TEST. INTERPOL permanece excluido. El canal solo se activa al integrar el PR de distribución.

Releases preparados: [motor 1.0.4](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.4) y [adaptador SRI 0.1.23](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.23). Los dos paquetes y manifiestos se verifican con firma/hash; los punteros permanecen en el PR hasta su integración.

La presencia de una versión en el canal permite su descarga firmada; la certificación documental requiere resultado, evidencia y ACK por trabajo real de ORDS.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Preparación de promoción C.151](docs/C151_PREPARACION_PRODUCCION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Canal TEST firmado](channels/test.json)
- [Canal PRODUCCION firmado](channels/production.json)
- [Reporte privado de seguridad](SECURITY.md)

No se alojan datos de sujetos, documentos obtenidos, evidencias ni secretos. Los assets se publican en Releases y se autentican mediante firmas de canal separadas para TEST y Producción.
