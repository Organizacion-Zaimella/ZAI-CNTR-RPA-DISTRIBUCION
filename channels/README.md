# Canales

La rama candidata C.145 publica la generación TEST 36 con motor `1.0.0-test.13` y los adaptadores enumerados en [VERSIONES_TEST.md](VERSIONES_TEST.md). `test.json` y `test.json.sig` son la fuente verificable; el inventario Markdown facilita la lectura humana. Verificar la firma y el commit antes de usarlo.

ORDS decide qué adaptadores y versiones requiere cada trabajo; la publicación no activa documentos ni equivale a certificación funcional. INTERPOL 0.1.1 solo está validado con fixtures de loopback, sin consulta real ni ACK. No hay canal productivo en este candidato.

Los futuros punteros de canal se acompañarán de firmas y apuntarán solo a Releases existentes y aprobados. Cada promoción requiere PR, revisión, firma y generación monotónica. No crear ni asumir `production.json` hasta que la política de confianza, custodia y release productiva esté aprobada.
