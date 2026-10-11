# Manifiestos de distribución — propuesta v1

**Estado C.145:** esta nota registra el diseño original; la afirmación de que T01 no publicaba manifiestos corresponde al estado inicial histórico. La rama candidata mantiene un canal TEST firmado generación 36 en channels/test.json/test.json.sig y releases versionados. Para interpretar la estructura efectiva, usar esos archivos, channels/VERSIONES_TEST.md, el contrato de publicación y la validación en el RPA candidato. Esta propuesta no es JSON Schema normativa.

El esquema futuro de canal incluirá: `schema_version`, canal, generación monotónica, publicación/caducidad, motor (versión, release, asset, tamaño, SHA-256, compatibilidad), adaptadores (ID, portal, versión, release, asset, tamaño, SHA-256, rangos de motor/contrato/OS), revocaciones y `signing_key_id`. Una firma separada cubrirá bytes canónicos del manifest.

El cliente valida propietario/repositorio fijados, firma, hash, compatibilidad, vigencia y revocación antes de ejecutar. Un SHA en JSON sin firma no autentica al publicador. El canal y los manifests de Releases son fuente ejecutable por su generación; confirmar firma/commit actual antes de promover. No hay canal productivo firmado en la línea C.145.
