# Adaptadores

La rama TEST contiene carpetas candidatas para los portales y funciones que ORDS asigna: IESS (2), SRI (3, 53), OFAC (5), SERCOP (11) e INTERPOL (12). Cada una tiene `src/`, `tests/`, `dependencies.lock`, `manifest.template.json` y README. Son **candidatos no certificados**; no deben habilitarse en Producción. Las pruebas públicas son sintéticas y no consultan portales ni contienen sujetos reales.

Los adaptadores Superintendencia (13–19) y Consejo de la Judicatura (73–76) permanecen en el repositorio RPA privado: ORDS TEST todavía marca esos documentos como semiautomáticos/ALTCHA o con evidencia esperada nula, por lo que la asignación automática 1.0.0 no es elegible. Documento 33 sigue sin implementación. No se copia ni publica código para esas funciones hasta resolver la elegibilidad y validar su función documental.
