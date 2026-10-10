# Canales

La rama `codex/sri-0.1.8-test14` prepara el canal TEST firmado generación 12 para validar `sri@0.1.8-candidate` junto al motor `1.0.0-test.5` y los adaptadores previamente asignados. El candidato incluye la app standalone, sidecar y dependencias fijadas. No es certificación ni habilitación de Producción. El puntero se mantiene en rama de QA; `main` y `production.json` no se modifican.

La generación 11 previa queda como base verificable en `codex/sri-0.1.7-test13`. Cada promoción requiere una generación superior, firma TEST, release inmutable y revisión del PR correspondiente.

La rama `codex/sri-0.1.9-test16` avanza el canal TEST firmado de generación 15 a 16 para `sri@0.1.9-candidate`, conservando los pins restantes. El release TEST firmado se publica bajo `cntr-rpa-sri-0.1.9-test16`. La app standalone obtuvo dos resultados MATCH, pero el candidato no se certifica hasta probar descarga y ejecución desde el motor con evidencia/ACK.
