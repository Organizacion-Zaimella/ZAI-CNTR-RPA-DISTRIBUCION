# Aplicación independiente SRI — candidato 0.1.12

Estado: **candidato privado 0.1.12, Gate A standalone aprobado; Gate B pendiente**. `app.py` ejecuta
documentos 3 y 53 con Playwright sin importar el motor CNTR. El motor no debe
recompilarse por esta aplicación.

## Requisitos

- Python 3.11 o posterior.
- Dependencia fijada en `dependencies.lock`.
- Microsoft Edge instalado; Google Chrome es fallback.
- Contexto JSON local suministrado por el harness autorizado de TEST. Contiene
  identificación y ubicación privada de evidencia: no versionarlo ni publicarlo.

## Ejecución local

```powershell
python -m pip install -r adapters/sri/dependencies.lock
python adapters/sri/app.py --context <RUTA_PRIVADA_AL_CONTEXTO_TEST>
```

El contexto tiene `document_id`, `entry_url` (la URL efectiva recibida de
ORDS), `identification`, `evidence_dir` y, opcionalmente, `pacing_seconds` y
`timeout_seconds`. La app solo acepta las rutas SRI acordadas para documentos
3 y 53, obliga al menos cinco segundos entre acciones y escribe capturas en la
ruta privada indicada. La salida JSON evita incluir identificación, nombre,
contenido de portal, URL, cookies y rutas locales; devuelve estado, motivo y
SHA-256 de la evidencia.

El sidecar registra tiempos por etapa y códigos de error saneados en un JSON
privado dentro del directorio de evidencias; nunca escribe URL, identificación
ni el texto de excepción. El ingreso usa una sola acción `fill` y verifica la
persistencia antes de consultar. Las pruebas sintéticas pasan en los dos
repositorios; la certificación integrada sigue pendiente. Los errores de
red/navegador se normalizan como `RETRYABLE`; la
salida no incluye el texto de la excepción. La aplicación identifica
`NETWORK_DISCONNECTED`, `NETWORK_CHANGED`, reset, rechazo, DNS, timeout y ruta
inalcanzable con códigos estables. En la ejecución integrada el motor registra
el intento como `REINTENTABLE/PORTAL_UNAVAILABLE` y avanza según el plan ORDS.
En un lote standalone, una navegación fallida se intenta una sola vez y la
siguiente pareja continúa en la misma instancia de navegador. La cobertura es
local y no sustituye la prueba externa del portal.

Si Playwright reporta error después de que la misma página llegó a la URL
exacta del documento y su formulario único está visible, el adaptador continúa
desde ese checkpoint sin volver a navegar. Si el formulario no está cargado,
conserva la causa reintentable y avanza al siguiente trabajo.

Los límites se separan por operación: navegación hasta `commit` 30 s;
visibilidad/interacción con controles 15 s; espera de habilitación del botón
hasta 15 s; respuesta del portal 45 s iniciales, ampliable en tramos de 15 s
cuando cambie el DOM o aparezca una señal explícita de carga, hasta un máximo
absoluto de 120 s; y estabilidad del resultado terminal durante 1 s. No son
pausas fijas: la app avanza en cuanto observa la postcondición. Las mediciones
SRI disponibles incluyen una corrida total de 28.7 s para docs. 3/53 pero no
desglosan tiempos por etapa; por eso estos son límites iniciales, no percentiles
estadísticos. Una desconexión explícita se clasifica de inmediato; una consulta
no concluyente al vencer su límite devuelve `RETRYABLE`, nunca ausencia. Un
resultado anterior o el texto explicativo fijo no cuenta como progreso; una
coincidencia positiva debe mostrar el identificador consultado en el contenido
del resultado.

En la ABI del sidecar, una barrera CAPTCHA/ALTCHA queda marcada durante el
lote: los otros documentos SRI del mismo lote se devuelven como
`HUMAN_REQUIRED` sin volver a navegar ni consultar.

Una respuesta positiva solo se acepta cuando el marcador del documento aparece
en el contenido principal visible y el RUC consultado aparece en ese mismo
contenido. El marcador sin identificación correlacionable queda
`RETRYABLE/MATCH_NOT_ATTRIBUTED`; no se guarda evidencia positiva ambigua.
La navegación espera `commit` para que la aplicación Angular no dependa de que
`DOMContentLoaded` termine.

El adaptador del sidecar también usa `type_text` pausado para activar los
eventos Angular, comprueba el valor de entrada y espera a que `Consultar` quede
habilitado antes del único envío. Una barrera detectada antes o después de
teclear se recuerda durante el lote y no se envía el formulario. Esta interfaz
se cubre con pruebas sintéticas y aún requiere una corrida integrada positiva.

## Candidato 0.1.12 — continuidad del lote tras error de red

El lote usa un único navegador y contexto para conservar cookies/sesión. Si un
documento termina con error de red o deja la pestaña inutilizable, el adaptador
crea una página nueva dentro del mismo contexto y continúa con el siguiente
documento en el orden recibido; no repite la consulta fallida ni reinicia el
navegador. Los cierres de target/contexto tienen códigos saneados. La prueba
standalone headed recorrió documentos 3 y 53 en orden y obtuvo `MATCH` en ambos,
con capturas PNG privadas válidas (61,472 y 106,364 bytes). Evidencia saneada:
`P01_SRI_STANDALONE_20261010_R7.json`. La suite standalone pasó 24 pruebas.
ORDS sigue asignando `sri@0.1.8-candidate`; no se cambió el pin, así que no se
declara ejecución integrada ni ACK de 0.1.12.

## Estado de certificación

La navegación de los documentos y la app standalone tienen evidencia positiva;
queda pendiente probar la versión 0.1.12 mediante el robot instalado. La
asignación TEST exacta vigente es 0.1.8-candidate y no se alteró. Esta versión
no se considera certificada para robot/ACK ni Producción.
