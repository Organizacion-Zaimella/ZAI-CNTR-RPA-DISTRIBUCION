# C.154 — motor 1.0.7 de Producción

La generación 8 del canal `PRODUCCION` publica el motor 1.0.7 desde el commit RPA
`fd6adb1a8b8294c7385dab64c5f26c9aa6a2c534`. Conserva las diez versiones de
adaptadores de la generación 7.

El motor incluye en una configuración los trabajos automáticos y los atendidos que
ORDS declaró elegibles, en su orden original. Ejecuta los automáticos en segundo
plano y abre los CAPTCHA/ALTCHA atendidos en primer plano. Conserva la evidencia
como `AUTOMATICA` o `ASISTIDA`, el journal y el ACK. Mantiene además el reintento
visible único de documentos automáticos que fallan ocultos por indisponibilidad o
tiempo de espera.

## Comprobaciones de publicación

- Release inmutable `cntr-rpa-engine-1.0.7` publicado antes del puntero de canal.
- ZIP, manifiesto y firma accesibles anónimamente con HTTP 200.
- ZIP SHA-256: `cdd15eae5d5aca0db1b292754715ee6c7af25f5964361595466ac28666b9188f`.
- EXE SHA-256: `dc24425ebda4e411e3744180f77fa7c346f05c60bcae035c808ba3f0918f1acb`.
- El empaquetador verificó firmas, hashes y monotonía de generación 7 a 8.
- El caso local de plan mixto verificó dos detalles en orden con modos `VISIBLE` y
  `HEADLESS` respectivamente. No representa una consulta real a los portales.

Tras integrar el PR del canal, el lanzador instalado con `PRODUCCION` detectará la
generación 8 y descargará el motor sin reinstalar. Se debe comprobar en la primera
ejecución real el número de trabajos elegibles, los resultados y ACK por detalle.
