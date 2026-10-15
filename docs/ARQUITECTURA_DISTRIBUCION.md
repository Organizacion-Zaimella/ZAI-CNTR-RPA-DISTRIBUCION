# Arquitectura de distribución

**Estado vigente C.145:** la infraestructura no está en estado inicial. El canal TEST y su firma publican la generación 36; el inventario y SHA están en [VERSIONES_TEST](../channels/VERSIONES_TEST.md). No existe canal de Producción en esta línea. Confirmar rama/SHA y firma antes de promover. El motor actual es genérico Python + Playwright; OpenClaw/workflows son legado.

## Responsabilidades

El desarrollo del motor y adaptadores se conserva en el repositorio de trabajo privado `Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA`. Oracle/ORDS conserva reglas, catálogo, sujetos, elegibilidad, orden, sesiones, estado y auditoría. Este repositorio público contendrá únicamente documentación publicable y, tras certificación, código depurado de adaptadores, manifiestos firmados y assets de GitHub Releases.

El launcher estable consultará un canal fijado localmente, validará firma, procedencia, digest, compatibilidad y revocación antes de instalar motor o adaptadores. El motor ejecutará el plan recibido de ORDS; un manifest público no decide qué sujeto o documento corresponde procesar.

## Autoridad de versiones y compatibilidad con ORDS

La selección funcional y la selección del artefacto son responsabilidades distintas:

- **ORDS define el trabajo:** elegibilidad, sujeto, documento, orden, `adapter_id` y `function_id` (por ejemplo, `sri` + `documento_3`). Puede publicar una versión de referencia o un rango de compatibilidad para diagnóstico/compatibilidad; esa referencia no debe convertirse por defecto en un pin exacto que bloquee el arranque.
- **El canal firmado define el artefacto vigente:** por ambiente selecciona la versión aprobada de cada adaptador, su hash, firma, ABI/contrato compatible y revocaciones. El launcher instala la versión vigente de ese canal antes de ejecutar.
- Cuando la versión informada por ORDS está atrasada, el motor usa la versión firmada más reciente del canal permitido **si** conserva `adapter_id`, `function_id` y el contrato/ABI que el trabajo necesita. Registra la versión ORDS recibida y la versión efectivamente ejecutada.
- El motor nunca ignora el plan de ORDS ni inventa otra función, documento, sujeto u orden. Tampoco descarga una versión arbitraria de GitHub Releases: solo activa el artefacto del canal firmado, compatible y no revocado.
- Si no existe el adaptador/función solicitado, hay incompatibilidad de ABI, una restricción explícita de versión, una revocación o falla la verificación criptográfica, no se ejecuta otra función como sustituto. Se registra un error de compatibilidad acotado al trabajo y se continúa con los trabajos independientes según el plan.
- Una actualización compatible de código de adaptador requiere publicar el Release y promover el canal del ambiente; no requiere actualizar ORDS. ORDS se cambia cuando cambia la asignación documento→adaptador/función, elegibilidad/orden, contrato de datos, rango mínimo compatible o una decisión explícita de pin/congelamiento/rollback.
- La misma separación aplica al motor: el canal autorizado selecciona la versión del motor. ORDS no selecciona ni fija la versión del ejecutable.
- Para mostrar el estado vigente sin acoplar releases, la consola/telemetría del robot reporta motor y adaptador desde el canal/estado instalado; ORDS expone su propia versión de API/paquete. No se debe usar el número de versión de ORDS como si fuera la versión del adaptador.

Los contratos actuales transmiten una versión de adaptador y la implementación C.153 todavía exige igualdad exacta contra el canal en el preflight. Esta sección define la política objetivo; la relajación del pin y la resolución compatible requieren un cambio de implementación versionado, pruebas de compatibilidad, rollback y promoción independiente. Hasta que ese cambio exista en el motor instalado, la igualdad exacta sigue siendo el comportamiento efectivo.

## Separación de versiones

El motor 1.0.0 y cada adaptador tendrán versiones independientes. El contrato de adaptadores y el formato de manifest se definen en `contracts/`. Los binarios y ZIP certificados se alojarán como assets de Releases; Git no contendrá ejecutables.


## Límites de certificación

La inclusión de un adaptador en el canal indica que el paquete puede descargarse y verificarse dentro de su ambiente; no acredita por sí sola ejecución real de portal, evidencia/ACK ni habilitación productiva. INTERPOL 0.1.1 permanece limitado a fixtures loopback y sin consulta real/ACK. Ningún dato de sujetos, credenciales ni evidencia real se publica aquí.
