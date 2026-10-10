# Contratos de manifiestos

El esquema activo del canal se encuentra en `channel.schema.json`. El archivo `channels/test.json` y su firma detached contienen los punteros TEST vigentes; la firma Ed25519 cubre los bytes canónicos UTF-8 del JSON. La clave se selecciona mediante `signing_key_id` y debe estar anclada en el launcher; nunca se descarga de GitHub ni se toma de la configuración local.

Los manifiestos de release contienen procedencia, commit, activos, tamaño, hashes y firmas. Los verificadores del actualizador validan los contratos antes de instalar. El schema no contiene ni define elegibilidad de sujetos o documentos: eso corresponde a Oracle/ORDS.
