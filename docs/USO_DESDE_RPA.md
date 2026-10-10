# Uso anónimo desde CNTR RPA

El cliente fija el propietario `Organizacion-Zaimella` y el repositorio `ZAI-CNTR-RPA-DISTRIBUCION`. Los archivos de canal y assets de GitHub Releases se leen por HTTPS sin cuenta, token ni cookie de GitHub.

El launcher solicita el canal configurado (`TEST` o `PRODUCCION`) desde la rama de distribución aprobada, valida firma Ed25519 anclada, generación, caducidad, revocación, compatibilidad, tamaño y SHA-256 antes de instalar. Descarga solo assets de Releases de este repositorio. No instala dependencias con `pip` desde Internet durante el arranque.

La instalación se realiza en staging por versión y activa el paquete validado de forma atómica. Conserva configuración, OAuth, journal y logs; ante fallo mantiene o restaura la última versión verificada. Una interrupción de red no autoriza omitir firmas, ejecutar versiones revocadas ni degradar una actualización obligatoria.

## Candidato TEST vigente

La rama `codex/c144-sri-test` contiene el puntero firmado del canal TEST para el motor 1.0.0 y el candidato SRI 0.1.13, documentos 3 y 53. Es una publicación de pruebas para C.144. No representa aprobación ni habilitación de Producción. La rama principal no apunta a este candidato; no existe canal `PRODUCCION` en este expediente.
