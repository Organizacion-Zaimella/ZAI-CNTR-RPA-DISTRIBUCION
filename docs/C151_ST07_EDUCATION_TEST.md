# C.151-ST07 — candidatos educativos TEST

Fecha: 2026-11-16. Estado: candidatos firmados para integración y QA en TEST; no promovidos a Producción.

| Adaptador | Versión | Release TEST | Función | Fuente RPA |
|---|---|---|---|---|
| Servicios Educación | `0.1.3-candidate` | `cntr-rpa-servicios-educacion-0.1.3-test2` | `documento_9` | `0be1b28849f93f75d7cbbcbd0ad194dcfed56119` |
| SENESCYT | `0.1.6-candidate` | `cntr-rpa-senescyt-0.1.6-test2` | `documento_10` | `0be1b28849f93f75d7cbbcbd0ad194dcfed56119` |

El canal TEST candidato es generación `130` y conserva el motor `1.0.29-test.1`. El gate público `verify_public_channel.py` aprobó sus 13 componentes: descargas anónimas, manifiestos, firmas, SBOM y ZIP. El canal de Producción no fue modificado.

La integración ORDS aún debe verificar la consulta, la evidencia y el ACK por cada trabajo elegible. El conjunto temporal de sujetos para QA no se publica en este repositorio; los identificadores, nombres y evidencias permanecen en almacenamiento privado.

La etiqueta `test1` de cada adaptador se conserva como Release sin referencia en el canal: el gate encontró que publicaba el SBOM con un nombre de archivo que el verificador no acepta. `test2` publica el archivo como `sbom.json`; no cambia el código del adaptador respecto del mismo commit fuente.
