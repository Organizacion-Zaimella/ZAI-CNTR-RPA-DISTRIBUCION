# Aplicación privada Consejo de la Judicatura

Versión candidata actual `0.1.2`, contrato IPC 1. `DOCUMENT_FUNCTIONS` expone una función para cada ID técnico 73–76 según el handler histórico [`judicatura_v1.py` en `627842b`](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/blob/627842b77dd582798917a410c929d96c635e8540/src/cntr_rpa/v2/handlers/judicatura_v1.py). La asociación entre esos IDs, la denominación funcional del catálogo y la captura del responsable sigue en conciliación; no inferirla del orden de la lista.

`app.py --context <JSON-privado>` es la aplicación Python/Playwright standalone. Recibe trabajos en el orden proveniente del plan autorizado; no consulta ORDS ni contiene registros de sujetos. Ejecuta el lote con una misma página Playwright y aplica una pausa mínima de cinco segundos entre navegación, escritura y clic. Confirma que el valor permanezca en el campo, acepta positivo solo con fila judicial visible y fecha, y negativo solo con mensaje explícito. La espera de resultados inicia en 60 s y se amplía en intervalos de 30 s, hasta 120 s, solo si señales de página/transferencia cambiaron durante los últimos 10 s; sin progreso devuelve `RETRYABLE`. Permite un único clic de recuperación tras tres segundos, únicamente si PrimeFaces informa cola AJAX vacía y el dato sigue intacto; no repite mientras exista actividad. Ante reCAPTCHA visible devuelve `HUMAN_REQUIRED`; error/timeout jamás se convierte en `NO_MATCH`. PNG de página completa se escribe en ruta privada.

El archivo de contexto debe mantenerse fuera del repositorio y contener `portal_id=6`, `evidence_dir` y `works[]` con `document_id` (73–76), `entry_url` y `subject` (`identification` y `display_name`; opcionales `names`, `surnames`, `type`, `origin`). En la ejecución integrada se reciben `execution_id` y `detail_id` reales. Para QA standalone sin ejecución ORDS, declarar `standalone_mode=true` y omitir ambos; la aplicación usa correlaciones locales solo para nombres de archivos privados. No imprimir el archivo ni guardar identidades o evidencias en Git.

```powershell
python app.py --context C:\ruta-privada\judicatura-plan.json
```

La salida estándar solo contiene ID documental, estado, motivo estable y SHA-256 de la evidencia. El modo headed se habilita con `--headed`; no resuelve CAPTCHA ni acepta términos.

La barrera reCAPTCHA se recuerda durante el lote del sidecar: después del
primer `HUMAN_REQUIRED`, los demás documentos de esa sesión quedan
`HUMAN_REQUIRED` sin volver a navegar ni pulsar el portal, para que el motor
pueda continuar con el siguiente grupo/portal del plan ORDS.

Estado: **candidato privado `0.1.2`; no aprobado para publicación pública ni release**. La versión `0.1.1-candidate` ya produjo resultados standalone para IDs 73–76 con evidencia PNG privada íntegra; los hashes y la clasificación constan en [P04](../../docs/v1.0.0/tareas/P04_JUDICATURA_STANDALONE_20261010_R1.json). La suite sintética de la lógica de espera progresiva tiene 14 casos aprobados. No se ejecutó otra búsqueda para retestar este ajuste. El snapshot Oracle TEST actual muestra los pares Judicatura no elegibles, sin asignación de adaptador; no se crean ejecuciones ni se fuerzan reglas. La integración RPA/ACK, la conciliación de nombres del catálogo y la certificación de `0.1.2` siguen pendientes.
