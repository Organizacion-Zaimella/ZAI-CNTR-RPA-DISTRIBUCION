# Publicación C.180/C.181 — Producción

- Fecha: 2026-10-21 (America/Guayaquil).
- Resultado: QA TEST aprobado y artefactos estables firmados publicados. El canal pasa a generación 26 mediante el PR de distribución asociado; la activación se confirma después de integrar ese PR.

## Cambios

- C.180: `ministerio_interior` muestra la alerta atendida solo cuando identifica un CAPTCHA visible sin resolver. Los falsos positivos por sujeto e iframe oculto quedan cubiertos por pruebas locales.
- C.181: el motor filtra solo el aviso recuperable `Xref table not zero-indexed...`; mantiene `strict=True` y rechaza PDFs corruptos.
- No se modificó ORDS ni se hizo una ejecución documental en Producción.

## Prueba integrada en TEST

- Canal usado: generación TEST `110`, motor `1.0.25-test.1`, adaptador `ministerio_interior@0.1.9-candidate`.
- Corrida ORDS: ejecución `1927`, configuración `845`, ambiente TEST, estado `COMPLETADA`.
- Dos detalles de documento 4 (`2641`, `2642`) terminaron `COMPLETADO` y recibieron `ACKED`.
- El robot mantuvo una sesión de navegador para los dos sujetos; el operador resolvió el CAPTCHA visible durante la corrida.
- Oracle TEST confirmó evidencias activas `1100`, `1101` y archivos activos `13970325`, `13970326`.
- Las pruebas locales de `adapters/ministerio_interior/tests/test_local_playwright.py` terminaron `16 passed`. La suite `tests/v100` terminó `28 passed`; las pruebas combinadas de constructor, firma y actualizador terminaron `30 passed`.
- La suite heredada completa tuvo `230 passed, 3 failed`: dos expectativas obsoletas de versión del instalador y un gate del runner que no encontró `Get-FileHash`. No son fallos del alcance C.180/C.181; están descritos en `qa/tareas/C.181/reports/informe_qa.md`.
- La búsqueda del aviso xref en los logs privados de la corrida 1927 no encontró coincidencias.

## Artefactos firmados

| Componente | Release/tag | SHA-256 del ZIP | Fuente |
|---|---|---|---|
| Motor `1.0.25` | `cntr-rpa-engine-1.0.25` | `0e8ced6f22b312742ad7f007ff204d48eb392d250dd73ddb39b14d7aec2a7a7f` | RPA `3bad69a37714de6f6c7596ca5e1c5f8575905e5b` |
| Ministerio del Interior `0.1.9` | `cntr-rpa-ministerio_interior-0.1.9` | `053f8f9801aec8a2a2b32709c551956024f87c2cb8ffd8f208ef2bdbe22b4406` | Adaptador `1d66cfc9744c3f7b2b27a4feb88fcb6c55d9f092` |

Los ZIP, manifiestos, firmas y SBOM se descargaron de GitHub sin autenticación. Las respuestas fueron HTTP 200 y coincidieron con los SHA-256, tamaños y firmas del trust root. El ejecutable del motor `CNTR-RPA-100.exe` tiene SHA-256 `8bb8a3812abac484dcd3ed0473c0c52289c713f369c83505cd4469ff49c789dc`.

## Canal firmado

- Canal: `PRODUCCION`, generación `26`.
- Motor: `1.0.25`.
- Adaptador: `ministerio_interior@0.1.9`.
- SHA-256 del JSON de canal: `4512dc7c73dcaff8deb6444b80ded4f94e6c1b7e6c73ef0a453184d94ba69cd1`.
- Trust root: `cntr-prod-63f2371d344a`.
- Se conservaron las otras nueve asignaciones de adaptadores y las cuatro revocaciones de generación 25.
- El launcher existente actualiza motor y adaptador al iniciarse; no se necesita reinstalarlo.

La publicación del Release hace disponibles los assets; el robot adopta la versión nueva cuando la PR del canal firmado se integra en `main`. Después del merge se registra aquí el SHA de `main` y el resultado de la lectura pública del canal.
