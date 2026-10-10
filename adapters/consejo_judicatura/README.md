# Consejo de la Judicatura — adaptador Python independiente

Versión candidata `0.1.1`; portal técnico 6; documentos 73–76. `adapter.py`
implementa `DOCUMENT_FUNCTIONS` para actor/demandado por identificación y por
nombres. `app.py --context <JSON-privado>` ofrece ejecución standalone con
Playwright; conserva una página durante el lote, respeta el orden recibido,
aplica al menos cinco segundos entre interacciones y guarda capturas PNG
completas fuera del repositorio.

El adaptador usa la URL del paso 1 del documento, valida el host/ruta de eSATJE,
comprueba que el dato permanezca en el campo y solo acepta un resultado positivo
cuando hay una fila judicial con fecha. Acepta `NO_MATCH` únicamente ante el
mensaje explícito del portal. Ante un resultado no verificado devuelve
`RETRYABLE`; un reCAPTCHA visible devuelve `HUMAN_REQUIRED` y no se resuelve ni
se evade. Una recuperación de clic único ocurre solo si el valor sigue intacto
y PrimeFaces confirma que su cola AJAX está vacía.

## Estado de validación

Gate A standalone ejecutado en TEST para los cuatro documentos: 73 y 74 dieron
`NO_MATCH` con capturas completas; 75 y 76 dieron `MATCH` con capturas
completas. Se emplearon sujetos ya existentes y una sesión por lote; los datos,
capturas, rutas y hashes privados no se incluyen aquí. El resultado saneado está
en el expediente RPA `P04_JUDICATURA_STANDALONE_20261010_R1.json`.

Gate A standalone está aprobado para TEST y el paquete `0.1.1-candidate` se
publicó firmado en [cntr-rpa-judicatura-0.1.1-test2](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.1-test2).
La fuente funcional corresponde al commit RPA `b6f77c1075fa81f4cfbab531f3f188cbed176ca8`;
el asset incluye la aplicación, el handler y dependencias fijadas, con SBOM,
SHA-256 y firma limitada al canal TEST.

La lectura GET-only actual de ORDS no muestra asignación de adaptador ni pares
elegibles para Judicatura. Por eso la publicación no afirma ejecución desde el
robot, evidencia/ACK ORDS ni certificación integrada. El manifiesto fuente
permanece `NOT_APPROVED` para evitar confundir el candidato TEST standalone con
una aprobación productiva.

## Uso standalone

El contexto privado debe incluir `portal_id=6`, `standalone_mode=true`,
`evidence_dir` y una lista `works[]` ordenada con `document_id` (73–76),
`entry_url` y `subject` con `identification` y `display_name`. No guardar ese
contexto ni las evidencias en Git.

```powershell
python app.py --context C:\ruta-privada\judicatura-plan.json --headed
```

Las pruebas locales son sintéticas y están en `tests/`; no consultan portales ni
ORDS.
