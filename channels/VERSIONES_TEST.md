# Versiones efectivas — canal TEST 62

Rama candidata de distribución C.151: `codex/c151-supercias-test37`. La fuente ejecutable es [`test.json`](test.json) con su [firma](test.json.sig). Producción sigue separada y sin cambios.

| Componente | Versión TEST | Release público |
|---|---|---|
| Motor | `1.0.0-test.16` | [`cntr-rpa-engine-1.0.0-test.16`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.0-test.16) |
| Fiscalía | `0.1.4-candidate` | [`cntr-rpa-fiscalia-0.1.4-test45`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-fiscalia-0.1.4-test45) |
| Ministerio del Interior | `0.1.1-candidate` | [`cntr-rpa-ministerio_interior-0.1.1-test46`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ministerio_interior-0.1.1-test46) |
| Superintendencia | `0.1.13-candidate` | [`cntr-rpa-supercias-0.1.13-test62`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.13-test62) |
| Judicatura | `0.1.7-candidate` | [`cntr-rpa-judicatura-0.1.7-test49`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.7-test49) |
| IESS | `0.1.6-candidate` | [`cntr-rpa-iess-0.1.6-test33`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-iess-0.1.6-test33) |
| INTERPOL | `0.1.1-candidate` | [`cntr-rpa-interpol-0.1.1-test36`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-interpol-0.1.1-test36) |
| Lista Clinton | `0.1.4-candidate` | [`cntr-rpa-lista-clinton-0.1.4-test21`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-lista-clinton-0.1.4-test21) |
| OFAC | `0.2.4-candidate` | [`cntr-rpa-ofac-0.2.4-test30`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ofac-0.2.4-test30) |
| SERCOP | `0.1.1-candidate` | [`cntr-rpa-sercop-0.1.1-test31`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sercop-0.1.1-test31) |
| SRI | `0.1.22-candidate` | [`cntr-rpa-sri-0.1.22-test34`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.22-test34) |
| Servicios Educación — documento 9 | `0.1.0-candidate` | [`cntr-rpa-servicios-educacion-0.1.0-test58`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-servicios-educacion-0.1.0-test58) |
| SENESCYT — documento 10 | `0.1.0-candidate` | [`cntr-rpa-senescyt-0.1.0-test59`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-senescyt-0.1.0-test59) |

Los adaptadores Superintendencia 0.1.13, Servicios Educación 0.1.0 y SENESCYT 0.1.0 están firmados en TEST y comprobados localmente contra hash, manifiesto y canal. Superintendencia 0.1.13 captura el PDF abierto en respuesta directa, descarga o pestaña nueva desde el mismo clic de la fila `RL`; la recuperación valida mismo origen y limita la consulta de la pestaña a un intento. Sus pruebas de portal real y ACK siguen pendientes. El motor `1.0.0-test.16` no cambió.

Servicios Educación 0.1.0 recupera el prototipo histórico `EducationTitlesV1` para `documento_9`; SENESCYT 0.1.0 adapta `documento_10`. Sus escenarios Playwright locales verifican `MATCH`, `NO_MATCH`, estado ambiguo y PNG. Oracle TEST confirma que el paso 1 de documento 10 usa `titulos-edusuperior.minedec.gob.ec`; `www.senescyt.gob.ec` permanece como URL informativa del portal y no decide navegación.

Fiscalía 8 cuenta con una corrida robot/ORDS exitosa registrada. Ministerio 4, Superintendencia 13–19 y Judicatura 6 aún requieren completar sus pruebas reales en el robot con evidencia/ACK. Ningún paquete nuevo habilita Producción. INTERPOL 12 conserva su barrera de autorización.

