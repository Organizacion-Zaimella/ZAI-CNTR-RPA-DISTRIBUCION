# Manifiestos de distribución — propuesta v1

El esquema futuro de canal incluirá: `schema_version`, canal, generación monotónica, publicación/caducidad, motor (versión, release, asset, tamaño, SHA-256, compatibilidad), adaptadores (ID, portal, versión, release, asset, tamaño, SHA-256, rangos de motor/contrato/OS), revocaciones y `signing_key_id`. Una firma separada cubrirá bytes canónicos del manifest.

El cliente validará owner/repo fijos, firma, hash y compatibilidad antes de ejecutar. Un SHA incluido en un JSON sin firma no autentica al publicador. Los tipos, canonicalización, política de caducidad y JSON Schema son trabajo posterior. **No se publican manifiestos activos en T01.**
