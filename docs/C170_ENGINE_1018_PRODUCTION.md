# C.170 — motor 1.0.18 y launcher 1.0.8 en Producción

El canal PRODUCCIÓN generación 18 cambia exclusivamente el motor a `1.0.18`. Conserva los diez adaptadores, sus funciones, la lista de revocación y el contrato de la generación 17. Fuente RPA: `833ff69d67f6ff552b12b7c704dc0ba61a8d5d1b`, integrado en `main` por el PR #59.

- Release del motor: `cntr-rpa-engine-1.0.18`; ZIP SHA-256 `16319266336714823dbab646383f4da8cad33b83b9518c201b69214626a5d6aa`.
- EXE del motor: versión CLI `1.0.18`, SHA-256 `ce4d1c7dc945407e99fe38cbe9142fa35e20944459084c62c04634a1e88ca155`.
- Release separado del instalador: `cntr-rpa-setup-1.0.8`, EXE SHA-256 `b6f2a52c5ca694d0a1575889121a150fe52cee228f2d45dafd6e5ca2b21e22aa`. Contiene el launcher nuevo y el motor 1.0.18. El launcher no se actualiza al cambiar solo el motor del canal.
- El instalador contiene cero credenciales. Reutiliza los archivos OAuth locales existentes en el equipo y solicita el usuario APEX.
- ZIP del motor, instalador y sus manifiestos/firmas recuperados anónimamente con HTTP 200; firma Ed25519, SHA-256 e inventario del motor comprobados.
- La generación TEST 99 descargó y activó el mismo EXE del motor en un sandbox, consultó las asignaciones ORDS TEST de solo lectura y verificó seis adaptadores. La regresión local de arranque, referencia ORDS atrasada/ausente/inválida, ejecución sidecar y ACK sintético aprobó. No se realizó una nueva consulta documental real ni un ACK ORDS TEST de C.170.
- El instalador QA 1.0.8 se probó en una instalación aislada: preparó una configuración sintética local, colocó launcher y motor con los hashes esperados y abrió sus CLI. Se desinstaló la copia QA y se restauró el acceso directo de la instalación habitual.
- El instalador EXE no tiene firma Authenticode; su integridad se publica mediante un manifiesto SHA-256 firmado con la clave Ed25519 de Producción. El usuario debe obtenerlo desde el Release indicado.

Antes de comunicar el pase al usuario, verificar que `channels/production.json` y su firma se sirvan desde `main` como generación 18 y que la ejecución inicial muestre motor 1.0.18. La primera corrida real de MRGUILLCA requiere observación de resumen, evidencia y ACK; la publicación no acredita por sí sola la descarga de sus documentos.
