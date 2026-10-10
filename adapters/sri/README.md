# Aplicación independiente SRI — candidato 0.1.10

Estado: **candidato privado 0.1.10, no certificado**. `app.py` ejecuta
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

Los límites se separan por operación: navegación hasta `commit` 45 s;
visibilidad/interacción con controles 30 s; espera de habilitación del botón
30 s; respuesta del portal hasta 120 s; y estabilidad visual del resultado
250 ms. PDF usa el máximo genérico de adquisición de artefacto de 120 s. No
son pausas fijas: la app avanza en cuanto observa la postcondición. El límite
de 30 s evita la espera implícita de Playwright (que podía agregar otros 30 s
al botón si Angular lo reemplazaba). Las corridas SRI exitosas registradas
duraron 7.864–12 s; ese historial sustenta el máximo de 30 s para controles y
el mayor margen de 120 s solo para una respuesta asíncrona o un artefacto. Una
desconexión explícita se clasifica de inmediato; una consulta no concluyente
al vencer su límite devuelve `RETRYABLE`, nunca ausencia. La app ignora el
indicador visible `Espere por favor`/carga. El texto explicativo fijo no cuenta
como resultado; una coincidencia positiva debe mostrar el identificador
consultado en el contenido del resultado.

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

## Retest TEST independiente 0.1.10

El 2026-10-10, la aplicación Python `0.1.10-candidate` recorrió los documentos
3 y 53 en ese orden, con una sola sesión/página headed de Chrome, y obtuvo
`MATCH` para ambos. Generó PNG completas privadas (67,566 bytes y 106,364
bytes); no se incluyen en este repositorio. El intervalo entre capturas fue
32.4 s y no representa la duración individual de cada página. El registro
saneado de resultados está en [RUN5 del PR de integración RPA](https://github.com/Organizacion-Zaimella/ZAI-RPA-CTRL-CAPTURA-INFORMACION-PUBLICA/blob/codex/cntr-rpa-1.0.0-integration/docs/v1.0.0/tareas/P01_SRI_RETEST_20261010_RUN5.json).

La ejecución identificó que Angular podía reemplazar el botón y que una
consulta `is_enabled()` heredaba el timeout implícito de Playwright. La versión
0.1.10 limita controles y habilitación a 30 s, con observaciones cada 250 ms;
la suite del adaptador pasó 21 pruebas. La liberación firmada de este candidato
está pendiente. ORDS aún pide `0.1.8-candidate`, por lo que no se ejecutó el
robot con `0.1.10` ni se registró ACK para esta versión.

## Estado de certificación

La exploración interactiva confirmó que las pantallas de formulario públicas
cargan. Aún faltan lectura de la configuración elegible vigente de ORDS TEST,
consultas reales autorizadas de las rutas positivas/negativas, revisión de la
atribución del resultado al sujeto y el ciclo con el motor instalado/ACK. Por
ello no crear release ni promover este candidato como certificado.
