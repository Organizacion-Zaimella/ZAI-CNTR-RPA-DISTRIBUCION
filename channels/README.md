# Canales

La rama candidata C.145 publica la generación TEST 36 con motor `1.0.0-test.13` y siete adaptadores enumerados en [VERSIONES_TEST.md](VERSIONES_TEST.md). `test.json` y `test.json.sig` son la fuente verificable; el inventario Markdown facilita la lectura humana. Verificar la firma y el commit antes de usarlo.

ORDS decide qué adaptadores y versiones requiere cada trabajo; la publicación no activa documentos ni equivale a certificación funcional. INTERPOL 0.1.1 solo está validado con fixtures de loopback, sin consulta real ni ACK. El canal `production.json` firmado generación 1 se prepara para los cinco adaptadores usados por los diez documentos aprobados; excluye INTERPOL.

Los punteros de canal se acompañan de firmas y apuntan solo a Releases existentes. La raíz PROD es `cntr-prod-63f2371d344a`, Ed25519; el material público está en `security/production-root-20261011.json` y la clave privada permanece cifrada por DPAPI fuera de este repositorio y las instalaciones cliente. El puntero PROD se firmó como generación 1; para publicarlo en `main`, los cinco releases estables que referencia deben estar creados y sus assets deben verificarse públicamente contra los manifiestos.
