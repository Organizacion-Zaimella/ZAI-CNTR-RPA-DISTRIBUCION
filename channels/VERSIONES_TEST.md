# Versiones efectivas — canal TEST 43

Rama candidata de distribución C.151: `codex/c151-supercias-test37`. La fuente de verdad ejecutable es [`test.json`](test.json) con su [firma](test.json.sig); este inventario describe su contenido. Producción queda fuera de esta promoción.

| Componente | Versión TEST | Release público |
|---|---|---|
| Motor | `1.0.0-test.15` | [`cntr-rpa-engine-1.0.0-test.15`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.0-test.15) |
| Fiscalía | `0.1.3-candidate` | [`cntr-rpa-fiscalia-0.1.3-test43`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-fiscalia-0.1.3-test43) |
| Superintendencia | `0.1.2-candidate` | [`cntr-rpa-supercias-0.1.2-test37`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.2-test37) |
| Judicatura | `0.1.5-candidate` | [`cntr-rpa-judicatura-0.1.5-test28`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.5-test28) |
| IESS | `0.1.6-candidate` | [`cntr-rpa-iess-0.1.6-test33`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-iess-0.1.6-test33) |
| INTERPOL | `0.1.1-candidate` | [`cntr-rpa-interpol-0.1.1-test36`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-interpol-0.1.1-test36) |
| Lista Clinton | `0.1.4-candidate` | [`cntr-rpa-lista-clinton-0.1.4-test21`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-lista-clinton-0.1.4-test21) |
| OFAC | `0.2.4-candidate` | [`cntr-rpa-ofac-0.2.4-test30`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ofac-0.2.4-test30) |
| SERCOP | `0.1.1-candidate` | [`cntr-rpa-sercop-0.1.1-test31`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sercop-0.1.1-test31) |
| SRI | `0.1.22-candidate` | [`cntr-rpa-sri-0.1.22-test34`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.22-test34) |

Los Releases referenciados contienen el asset indicado y `release-manifest.json` con firma. El canal 43 se firmó con la raíz TEST registrada por el motor y se verificó con el validador del actualizador. La campaña instalada 1699 en modo `BACKGROUND` acreditó los diez documentos de SRI 3/53, IESS 2, OFAC 5/33, SERCOP 11 y Judicatura 73–76: 28 resultados concluyentes, 28 evidencias y 28 ACK. Fiscalía 0.1.3 es candidato C.151; su corrida Python real produjo `NO_MATCH` y `MATCH` con PNG, mientras su integración instalada y ACK aún requieren verificación. INTERPOL 12 no formó parte de esa campaña y conserva su barrera de autorización. El detalle está en el expediente C.145.

Para comprobar qué binario se ejecutará, leer `state/test/active.json`, verificar `engine.files["CNTR-RPA-100.exe"]` contra el SHA-256 de `engine.path/CNTR-RPA-100.exe` y usar esa ruta. Nunca elegir un EXE por nombre o por su ubicación aparente.


INTERPOL 0.1.1-candidate migra el workflow histórico 61/v2 para el documento 12. Su paquete y canal están firmados para TEST. La evidencia disponible es exclusivamente de páginas locales simuladas; la protección de autorización mantiene las URL externas bloqueadas y no se ejecutó consulta real ni ACK ORDS.
