
## Candidato TEST generación 13 — motor 1.0.0-test.6 — 2026-10-10

El prerelease `cntr-rpa-1.0.0-test.15` mantiene los pines de adaptadores del canal generación 12 (incluido SRI `0.1.8-candidate`) y actualiza solo el motor a `1.0.0-test.6`. Este build incluye navegación Playwright con `wait_until="commit"` acotado, necesaria para páginas cliente SPA que siguen renderizando después del commit HTTP. Se compiló aislado desde el commit RPA `ba64f1880a2c71fa0e25cf01cf82e21e637b488d`; CLI `--version` y `--preflight` pasaron. La suite del repositorio de distribución pasó 36/36. El canal y el paquete de motor tienen firma TEST y hashes verificados por el builder; SHA-256 del ZIP: `babf166e310dbc7bea5d566ab36cb54374a2f0a128d1eda2e8f8cae6694708c3`.

Es un candidato técnico para actualizar el motor aislado y repetir el E2E. No certifica todavía SRI ni aporta por sí solo evidencia/ACK ORDS. `main`, Producción y elegibilidad permanecen sin cambios.

## Candidato TEST generación 14 — motor 1.0.0-test.7 — 2026-10-10

El prerelease `cntr-rpa-1.0.0-test.16` incluye el build aislado del motor `1.0.0-test.7`, commit RPA `aa2a5412dd0ae73ba344266dca8ae2a8d99db9ba`. Combina navegación SPA acotada (`wait_until="commit"`) con la solicitud explícita de bytes crudos en descargas anónimas de GitHub Release. El canal parte de generación 13, preserva los cinco adaptadores y el pin SRI `0.1.8-candidate`, y pasa a generación 14. Builder y firmas TEST verifican manifiesto/canal/ZIP. La prueba anónima del actualizador aislado aún debe confirmar instalación y E2E SRI; no es certificación. El candidato `test.15` queda supersedido por el error HTTP 404 al descargar su manifest JSON. `main` y Producción no se modifican.
