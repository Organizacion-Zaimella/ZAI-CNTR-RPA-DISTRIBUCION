# Versiones efectivas — canal TEST 55

Rama candidata de distribución C.151: `codex/c151-supercias-test37`. La fuente de verdad ejecutable es [`test.json`](test.json) con su [firma](test.json.sig); este inventario describe su contenido. Producción queda fuera de esta promoción.

| Componente | Versión TEST | Release público |
|---|---|---|
| Motor | `1.0.0-test.16` | [`cntr-rpa-engine-1.0.0-test.16`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.0-test.16) |
| Fiscalía | `0.1.4-candidate` | [`cntr-rpa-fiscalia-0.1.4-test45`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-fiscalia-0.1.4-test45) |
| Ministerio del Interior | `0.1.1-candidate` | [`cntr-rpa-ministerio_interior-0.1.1-test46`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ministerio_interior-0.1.1-test46) |
| Superintendencia | `0.1.8-candidate` | [`cntr-rpa-supercias-0.1.8-test55`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.8-test55) |
| Judicatura | `0.1.7-candidate` | [`cntr-rpa-judicatura-0.1.7-test49`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.7-test49) |
| IESS | `0.1.6-candidate` | [`cntr-rpa-iess-0.1.6-test33`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-iess-0.1.6-test33) |
| INTERPOL | `0.1.1-candidate` | [`cntr-rpa-interpol-0.1.1-test36`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-interpol-0.1.1-test36) |
| Lista Clinton | `0.1.4-candidate` | [`cntr-rpa-lista-clinton-0.1.4-test21`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-lista-clinton-0.1.4-test21) |
| OFAC | `0.2.4-candidate` | [`cntr-rpa-ofac-0.2.4-test30`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ofac-0.2.4-test30) |
| SERCOP | `0.1.1-candidate` | [`cntr-rpa-sercop-0.1.1-test31`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sercop-0.1.1-test31) |
| SRI | `0.1.22-candidate` | [`cntr-rpa-sri-0.1.22-test34`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.22-test34) |

Los Releases referenciados contienen los assets firmados. La generación 55 fue verificada localmente con la raíz TEST. El motor `1.0.0-test.16` conserva en un resultado `ERROR` los códigos técnicos permitidos, incluido `PORTAL_UNAVAILABLE`; no agrega navegación específica de portal. Superintendencia 0.1.7 tuvo una corrida real previa con `PORTAL_UNAVAILABLE`; 0.1.8 cambia solo el recorrido de documento 16 y está pendiente de integración real/ACK. Fiscalía, Ministerio y Judicatura 6 tienen corridas standalone atendidas registradas en C.151, pero la descarga/ejecución desde el robot y evidencia/ACK por portal continúan pendientes. Ningún candidato habilita Producción. INTERPOL 12 conserva su barrera de autorización. El detalle está en el expediente C.151.

Para comprobar qué binario se ejecutará, leer `state/test/active.json`, verificar `engine.files["CNTR-RPA-100.exe"]` contra el SHA-256 de `engine.path/CNTR-RPA-100.exe` y usar esa ruta. Nunca elegir un EXE por nombre o por su ubicación aparente.


INTERPOL 0.1.1-candidate migra el workflow histórico 61/v2 para el documento 12. Su paquete y canal están firmados para TEST. La evidencia disponible es exclusivamente de páginas locales simuladas; la protección de autorización mantiene las URL externas bloqueadas y no se ejecutó consulta real ni ACK ORDS.
