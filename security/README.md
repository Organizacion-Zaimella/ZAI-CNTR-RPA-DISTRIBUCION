# Firma y revocación

Las claves privadas permanecen fuera del repositorio y de los equipos cliente. El launcher fija raíces de confianza embebidas; el registro público no puede sustituir esa confianza por sí solo.

La raíz de Producción `cntr-prod-63f2371d344a` (Ed25519) se registró para el candidato C.145 en [production-root-20261011.json](production-root-20261011.json). Su clave privada está cifrada mediante DPAPI para el usuario custodio y protegida por ACL local; nunca se publica. La clave TEST y la raíz PROD son distintas: un canal firmado por una no es aceptado por la otra. Las firmas verifican integridad/autenticidad del artefacto, no sustituyen la aprobación de una versión ni la certificación funcional.
