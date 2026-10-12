# C.151 — preparación de promoción a Producción

Fecha: 2026-10-12. Estado: **paquetes PROD publicados; canal de Producción pendiente de aprobación en GitHub**.

## Alcance

La autorización del usuario habilita preparar y publicar los seis adaptadores C.151 en el repositorio público. Se conserva el motor productivo existente 1.0.1. No se publican datos de sujetos, capturas reales, credenciales ni evidencia privada.

Cada Release contiene el ZIP candidato, `release-manifest.json`, su firma Ed25519 y `sbom-production.json`. Los manifiestos identifican el canal `PRODUCCION`, conservan la versión candidata para que no se confunda con una certificación funcional y declaran que ejecución real, evidencia ORDS y ACK siguen pendientes.

| Portal | Versión distribuida | Release PROD |
|---|---:|---|
| Consejo de la Judicatura | 0.1.7-candidate | [cntr-rpa-judicatura-0.1.7-prod1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.7-prod1) |
| Fiscalía General del Estado | 0.1.4-candidate | [cntr-rpa-fiscalia-0.1.4-prod1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-fiscalia-0.1.4-prod1) |
| Ministerio del Interior | 0.1.1-candidate | [cntr-rpa-ministerio_interior-0.1.1-prod1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ministerio_interior-0.1.1-prod1) |
| SENESCYT | 0.1.0-candidate | [cntr-rpa-senescyt-0.1.0-prod1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-senescyt-0.1.0-prod1) |
| Servicios Educación | 0.1.0-candidate | [cntr-rpa-servicios-educacion-0.1.0-prod1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-servicios-educacion-0.1.0-prod1) |
| Superintendencia de Compañías | 0.1.14-candidate | [cntr-rpa-supercias-0.1.14-prod1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.14-prod1) |

## Canal firmado

La promoción propuesta actualiza `channels/production.json` desde generación 2 a 3, mantiene el motor 1.0.1 y reemplaza Judicatura 0.1.5 por 0.1.7 para conservar en el mismo módulo la función nueva de documento 6 junto con los documentos 73–76. Los demás adaptadores productivos existentes se conservan.

La clave de Producción `cntr-prod-63f2371d344a` firmó la generación 3. La raíz pública está versionada en `security/production-root-20261011.json`; la clave privada permanece protegida localmente y no forma parte del repositorio.

El canal de la rama candidata verificó con la raíz pública anclada. La rama `main` exige al menos una aprobación de PR y aplica esa regla también a administradores. Hasta que el cambio sea revisado e integrado, generación 2 sigue siendo el canal activo; publicar Releases no cambia el puntero productivo.

## Oracle/ORDS y estado operativo

La lectura de Producción del 12-oct confirmó DB `ZAI`, `DATA.PK_CNTR_ORDS.VERSION = 1.0.0-rc.5`, y columnas `ADAPTADOR_FUNCION` y `ORDEN_SESION` presentes. Los documentos C.151 4, 6, 8, 9, 10 y 13–19 aún no tenían asignación; Judicatura 73–76 apuntaba a 0.1.5. Por tanto, la columna existe, pero ORDS sigue en rc.5 y debe avanzar al contrato rc.6 antes de asignar los adaptadores que necesita el robot.

No se ejecutó DDL ni DML productivo. No se abrió APEX ni se crearon ejecuciones. Las asociaciones de documento se prepararán en SQL versionado, con reversa y guardas de DB, y se aplicarán después de publicar el canal y el paquete ORDS requerido.

La protección de `main` exige una aprobación humana. No se intenta eliminar ni sortear esa protección. La integración pendiente no se declara como pase productivo completado.
