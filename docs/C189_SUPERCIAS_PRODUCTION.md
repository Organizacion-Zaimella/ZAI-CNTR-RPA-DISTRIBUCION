# C.189 — Superintendencia 0.1.18 en Producción

## Promoción

El adaptador estable `supercias@0.1.18` se construyó desde el paquete firmado y probado en TEST `supercias@0.1.18-candidate`, release `cntr-rpa-supercias-0.1.18-test1`. La validación funcional en TEST cubrió los documentos 17–19, con PDF y ACK en una sesión. El expediente del proyecto conserva el detalle privado de ejecución y cotejo de hashes de evidencia.

El código probado pertenece al commit RPA `a153ff51052ba6faf3e69ca4edb773e279ddcfd7`. El PR RPA #68 se integró como `6f041a1b33c057f29bcb6324e720845868f98d4b`; ambos tienen el mismo árbol fuente (`68c716864d9dcbf46505c59b993c6500675c79c5`).

| Elemento | Valor |
|---|---|
| Release TEST | `cntr-rpa-supercias-0.1.18-test1` |
| SHA-256 del paquete TEST | `c51c4a41ea0b8431e76be5dda66e5464bb34e551c10cfb03ac1c0eb7491285e6` |
| Release estable | [`cntr-rpa-supercias-0.1.18`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.18) |
| SHA-256 del paquete de Producción | `b9dc77dbbb97047d1e97161508e3d3715b25f506e8522860172907978df5305e` |
| SHA-256 del manifiesto de release | `a70b78d309ed88579edfbedd02a720abc0aa2fd5d40d0270ed8b89c8502e693e` |
| SHA-256 del SBOM | `e1499a003505606d61f6f07eea1fbb5e9c02c1e638c13656cc93ab7621a34198` |

Los cuatro assets de la release estable se descargaron anónimamente por HTTPS y devolvieron HTTP 200. El ZIP, manifiesto, firma Ed25519 y SBOM se verificaron contra hashes y la raíz PROD.

## Canal firmado

La propuesta de canal sube de generación 26 a 27, reemplaza solo `supercias@0.1.17` por `supercias@0.1.18`, y conserva motor `1.0.25`, los demás adaptadores y la lista de revocación. SHA-256 de `production.json`: `afc5c7158722411aca1e4279273de39263d459a6dfc9223b1097990737446316`. El canal está firmado con la raíz productiva `cntr-prod-63f2371d344a`.

La activación del canal ocurre al integrar `channels/production.json` y su firma en `main`; el PR de distribución registra ese cambio. No se ejecutó una configuración productiva ni se modificó ORDS. Al iniciar el launcher existente después de la activación, el actualizador consulta el canal y aplica el adaptador firmado sin reinstalar el robot.
