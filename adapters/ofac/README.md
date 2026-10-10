# Adaptador OFAC

Aplicación Python independiente para el documento Oracle `5` (búsqueda en
OFAC Sanctions List Search). Candidato `0.1.3-candidate`.

`app.py --context <JSON-privado>` ejecuta una búsqueda por nombre con Playwright
en el portal oficial. Separa esperas de navegación (máximo 30 s), controles
(máximo 30 s) y resultado (60 s iniciales; extensiones de 30 s mientras haya
señales de actividad, hasta 120 s total). Son límites de ejecución, no pausas
fijas: Playwright espera los controles visibles y el conteo estable. Deben
calibrarse con duraciones saneadas de ejecuciones reales por documento. Respeta
una pausa mínima de cinco segundos entre navegación, llenado y envío; no inicia
sesión ni evade CAPTCHA/controles. Solo
emite `MATCH` o `NO_MATCH` cuando la página presenta un conteo “Lookup Results:
N Found”. Espera explícitamente a que ambos controles estén visibles antes de
interactuar. La captura completa PNG se guarda fuera de Git y la salida contiene
solo estado, motivo y SHA-256.

En la ABI del sidecar, una barrera CAPTCHA queda marcada durante el lote:
los detalles restantes reciben `HUMAN_REQUIRED` sin otra navegación o envío.
En el ejecutor standalone `run_many`, la cola se detiene ante esa barrera para
que el orquestador continúe con el siguiente portal.

La inspección del 10-10-2026 abrió el formulario público y confirmó sus
controles y panel de resultados sin enviar una consulta. El snapshot GET-only
de ORDS TEST del mismo corte devolvió cero parejas OFAC elegibles, por lo que
no se generó una ejecución, evidencia documental ni ACK. No se infiere el estado
de otros documentos OFAC a partir de esa ausencia de trabajo. `DOCUMENT_FUNCTIONS.documento_5`
implementa el ABI del sidecar CNTR RPA 1.0.0; el motor conserva el orden de
trabajo y esta aplicación contiene la navegación específica OFAC.

## Ejecución local TEST

Instalar Playwright según `dependencies.lock` y utilizar Edge o Chrome instalado.
El contexto, el identificador, el nombre y las evidencias deben permanecer en
rutas locales privadas fuera del repositorio.

```powershell
python app.py --context C:\ruta-privada\ofac-document-5.json
```

El manifest continúa `NOT_APPROVED` hasta completar el Gate B de descarga
firmada anónima, ejecución con motor 1.0.0 instalado y ACK ORDS TEST.
