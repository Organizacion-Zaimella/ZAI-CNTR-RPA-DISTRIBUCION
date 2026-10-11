# Versiones efectivas — canal TEST 28

Rama de distribución: `codex/cntr-rpa-1.0.0-unified-test28`. La fuente de verdad ejecutable es [`test.json`](test.json) con su [firma](test.json.sig); este inventario describe su contenido. Producción queda fuera de esta promoción.

| Componente | Versión TEST | Release público |
|---|---|---|
| Motor | `1.0.0-test.12` | [`cntr-rpa-engine-1.0.0-test.12`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.0-test.12) |
| Judicatura | `0.1.5-candidate` | [`cntr-rpa-judicatura-0.1.5-test28`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.5-test28) |
| IESS | `0.1.3-candidate` | [`cntr-rpa-1.0.0-test.11`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-1.0.0-test.11) |
| INTERPOL | `0.1.0-candidate` | [`cntr-rpa-1.0.0-test.3`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-1.0.0-test.3) |
| Lista Clinton | `0.1.4-candidate` | [`cntr-rpa-lista-clinton-0.1.4-test21`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-lista-clinton-0.1.4-test21) |
| OFAC | `0.2.2-candidate` | [`cntr-rpa-ofac-0.2.2-test3`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ofac-0.2.2-test3) |
| SERCOP | `0.1.0-candidate` | [`cntr-rpa-1.0.0-test.3`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-1.0.0-test.3) |
| SRI | `0.1.21-candidate` | [`cntr-rpa-sri-0.1.21-test1`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.21-test1) |

Los ocho Releases responden públicamente y contienen el asset indicado y `release-manifest.json` con firma. El canal 28 se firmó con la raíz TEST registrada por el motor y se verificó con el validador del actualizador. La actualización instalada y la ejecución documental se acreditan por separado: versión activa en `state/test/active.json`, asignación exacta ORDS, resultado por documento, evidencia y ACK.

Para comprobar qué binario se ejecutará, leer `state/test/active.json`, verificar `engine.files["CNTR-RPA-100.exe"]` contra el SHA-256 de `engine.path/CNTR-RPA-100.exe` y usar esa ruta. Nunca elegir un EXE por nombre o por su ubicación aparente.
