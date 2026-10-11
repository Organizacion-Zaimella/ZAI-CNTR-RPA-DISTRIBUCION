# Canales

La generación TEST 23 reúne el motor `1.0.0-test.10` y las versiones de adaptadores
enumeradas en [VERSIONES_TEST.md](VERSIONES_TEST.md). `test.json` y `test.json.sig`
son la fuente verificable; el inventario Markdown facilita la lectura humana.
La rama es opt-in para TEST. ORDS decide qué adaptadores y versiones requiere cada
trabajo; la publicación no activa documentos ni equivale a certificación funcional.

Los futuros `test.json` y `production.json` se acompañarán de `test.json.sig` y `production.json.sig` y apuntarán solo a Releases existentes y aprobados. Cada promoción requiere PR, revisión, firma y generación monotónica. No se crean punteros en T01 porque no hay Releases certificados.
