# Canales

La generación TEST 21 firma `lista_clinton@0.1.4-candidate`, preserva los otros
adaptadores del canal verificado de generación 20 e incluye el prerelease
`cntr-rpa-lista-clinton-0.1.4-test21`. Es un candidato opt-in. El plan ORDS TEST
actual no tiene pareja elegible ni función asignada para documento 33; no
ejecutar el robot con una versión impuesta ni promover a Producción.

Los futuros `test.json` y `production.json` se acompañarán de `test.json.sig` y `production.json.sig` y apuntarán solo a Releases existentes y aprobados. Cada promoción requiere PR, revisión, firma y generación monotónica. No se crean punteros en T01 porque no hay Releases certificados.
