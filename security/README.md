# Firma y revocación

La clave privada de firma se custodia fuera de este repositorio y de las estaciones cliente. El launcher fija una raíz de confianza que no puede cambiarse editando un archivo público.

## Raíz de canal TEST

- Key ID: `cntr-test-a37738608946`
- Alcance: solo `TEST`; la clave no está autorizada para `PRODUCCION`.
- Algoritmo: Ed25519.
- Clave pública: `0IbODGytIK+0j8pcY5m5bM2hH37tbiuy8r3u3ZaMmZE=`
- El fingerprint se deriva como `SHA-256(clave pública)`; el ID usa los primeros 12 caracteres hexadecimales.
- La privada permanece protegida localmente con DPAPI y no se distribuye.

La firma del canal y del release manifest se valida contra esta raíz embebida en el launcher. La clave pública publicada aquí sirve para auditoría; no sustituye el ancla local.
