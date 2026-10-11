# Versiones efectivas — canal TEST 32

Rama de distribución: `codex/cntr-rpa-1.0.0-c145`. La fuente de verdad ejecutable es [`test.json`](test.json) con su [firma](test.json.sig); este inventario describe su contenido. Producción queda fuera de esta promoción.

| Componente | Versión TEST | Release público |
|---|---|---|
| Motor | `1.0.0-test.12` | [`cntr-rpa-engine-1.0.0-test.12`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.0-test.12) |
| Judicatura | `0.1.5-candidate` | [`cntr-rpa-judicatura-0.1.5-test28`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.5-test28) |
| IESS | `0.1.5-candidate` | [`cntr-rpa-iess-0.1.5-test32`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-iess-0.1.5-test32) |
| INTERPOL | `0.1.0-candidate` | [`cntr-rpa-1.0.0-test.3`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-1.0.0-test.3) |
| Lista Clinton | `0.1.4-candidate` | [`cntr-rpa-lista-clinton-0.1.4-test21`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-lista-clinton-0.1.4-test21) |
| OFAC | `0.2.4-candidate` | [`cntr-rpa-ofac-0.2.4-test30`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ofac-0.2.4-test30) |
| SERCOP | `0.1.1-candidate` | [`cntr-rpa-sercop-0.1.1-test31`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sercop-0.1.1-test31) |
| SRI | `0.1.21-candidate` | [`cntr-rpa-sri-0.1.21-test1`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.21-test1) |

Los Releases referenciados contienen el asset indicado y `release-manifest.json` con firma. El canal 32 se firmó con la raíz TEST registrada por el motor y se verificó con el validador del actualizador. La aplicación IESS 0.1.5 conserva la sesión entre sujetos y registra la respuesta visible «El RUC ingresado no es correcto» como `SIN_RESULTADO` con captura privada; su integración instalada y ACK se acreditan por separado, no por la publicación del paquete.

Para comprobar qué binario se ejecutará, leer `state/test/active.json`, verificar `engine.files["CNTR-RPA-100.exe"]` contra el SHA-256 de `engine.path/CNTR-RPA-100.exe` y usar esa ruta. Nunca elegir un EXE por nombre o por su ubicación aparente.
