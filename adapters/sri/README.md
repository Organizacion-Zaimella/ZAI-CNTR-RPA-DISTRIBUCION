# Aplicación independiente SRI — candidato 0.1.9

Estado: **candidato privado 0.1.9, no certificado**. `app.py` ejecuta
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

## Esperas: implementación y propuesta de calibración

La implementación candidata actual tiene estos topes: navegación `commit` 45
s, visibilidad/interacción con controles 45 s, habilitación del botón 30 s,
respuesta del portal 120 s y estabilidad visual del resultado 250 ms. El motor
instalado mantiene hasta 120 s para adquirir un PDF. Son límites máximos del
código; no son pausas que se consuman siempre. Corridas SRI anteriores dieron
7.864–12 s de duración total, pero no conservaron duración por etapa, por lo
que no prueban que esos topes sean óptimos.

Propuesta operativa para validar con telemetría saneada por etapa:

| Operación | Espera inicial | Extensión máxima | Señal de avance |
|---|---:|---:|---|
| Navegar o refrescar el URL del documento | 30 s a `commit` | 30 s adicionales, total 60 s | URL exacta confirmada y luego control del documento visible |
| Esperar controles dinámicos | 20 s | 10 s adicionales, total 30 s | Control visible/habilitado y valor persistido |
| Respuesta de consulta | 60 s | Dos extensiones de 30 s, total 120 s | Cambio del resultado visible, carga activa o respuesta de red pertinente |
| Inicio de PDF | 60 s | Hasta 120 s total si hay progreso | Evento de descarga o apertura de PDF |
| Completar/guardar PDF | 60 s | Hasta 120 s total si el archivo avanza | Descarga completada y archivo validable |

Estos valores son una propuesta inicial, no una certificación estadística. Se
deben ajustar por documento cuando haya suficientes duraciones reales; la
telemetría no debe incluir URL completa, identificación, nombres, texto del
portal, cookies ni rutas privadas. Playwright permite interactuar cuando los
controles están listos y las descargas distinguen el evento de inicio de la
finalización del archivo. Los errores de red explícitos se clasifican de
inmediato y una consulta no concluyente vence como `RETRYABLE`, nunca como
ausencia. La app ignora el indicador visible `Espere por favor`/carga. El texto
explicativo fijo no cuenta como resultado; una coincidencia positiva debe
mostrar el identificador consultado en el contenido del resultado.

En la ABI del sidecar, una barrera CAPTCHA/ALTCHA queda marcada durante el
lote: los otros documentos SRI del mismo lote se devuelven como
`HUMAN_REQUIRED` sin volver a navegar ni consultar.

Una respuesta positiva solo se acepta cuando el marcador del documento aparece
en el contenido principal visible y el RUC consultado aparece en ese mismo
contenido. El marcador sin identificación correlacionable queda
`RETRYABLE/MATCH_NOT_ATTRIBUTED`; no se guarda evidencia positiva ambigua.
La navegación espera `commit` para que la aplicación Angular no dependa de que
`DOMContentLoaded` termine.

La aplicación standalone usa tecleo pausado para activar los eventos Angular;
el sidecar usa `fill` en una acción y comprueba el valor de entrada. Ambos
esperan a que `Consultar` quede habilitado antes del único envío. Una barrera
detectada antes o después de ingresar el valor se recuerda durante el lote y no
se envía el formulario. Esta interfaz se cubre con pruebas sintéticas y aún
requiere una corrida integrada positiva.

## Estado de certificación

La exploración interactiva confirmó que las pantallas de formulario públicas
cargan. Aún faltan lectura de la configuración elegible vigente de ORDS TEST,
consultas reales autorizadas de las rutas positivas/negativas, revisión de la
atribución del resultado al sujeto y el ciclo con el motor instalado/ACK. Por
ello no crear release ni promover este candidato como certificado.
