# C.157 — Candidato del canal Producción

La aplicación Supercias 0.1.17 y el motor 1.0.11 proceden de los Releases firmados de TEST generación 89. La instalación aislada ejecutó el documento 16 con un sujeto existente de Oracle TEST: ejecución 1826, detalle 2540, `COMPLETADO`, evidencia asociada y ACK confirmado. Las capturas y datos del sujeto no se distribuyen.

| Componente | Canal anterior | Candidato | Release público |
|---|---|---|---|
| Motor | 1.0.10 | 1.0.11 | [cntr-rpa-engine-1.0.11](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.11) |
| Supercias | 0.1.16 | 0.1.17 | [cntr-rpa-supercias-0.1.17](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.17) |

`channels/production.json` generación 11 y `production.json.sig` están verificados con la raíz de confianza de Producción. Los assets publicados respondieron HTTP 200 sin autenticación: motor 74 160 295 bytes y adaptador 18 383 bytes. Su firma, hash y tamaño se comprobaron antes de preparar el canal. Los demás componentes son idénticos a generación 10.

La actualización del canal no modifica Oracle por sí misma. El documento 16 requiere asignación productiva `supercias@0.1.17:documento_16`, mediante script versionado y controlado. El motor 1.0.11 contiene la recuperación entre sujetos tras timeout; SENESCYT documento 10 requiere una nueva corrida real para confirmar su comportamiento en Producción.
