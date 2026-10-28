# Versiones efectivas — canal TEST

La fuente de verdad ejecutable es [test.json](test.json) y su [firma](test.json.sig). Este inventario corresponde a la generación 119.

| Componente | Versión | Release |
|---|---|---|
| Motor | `1.0.28-test.1` | [cntr-rpa-engine-1.0.28-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-engine-1.0.28-test1) |
| consejo_judicatura | `0.1.8-candidate` | [cntr-rpa-judicatura-0.1.8-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-judicatura-0.1.8-test1) |
| fiscalia | `0.1.9-candidate` | [cntr-rpa-fiscalia-0.1.9-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-fiscalia-0.1.9-test1) |
| iess | `0.1.6-candidate` | [cntr-rpa-iess-0.1.6-test33](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-iess-0.1.6-test33) |
| interpol | `0.1.1-candidate` | [cntr-rpa-interpol-0.1.1-test36](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-interpol-0.1.1-test36) |
| lista_clinton | `0.1.5-candidate` | [cntr-rpa-lista-clinton-0.1.5-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-lista-clinton-0.1.5-test1) |
| ministerio_interior | `0.1.9-candidate` | [cntr-rpa-ministerio-interior-0.1.9-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ministerio-interior-0.1.9-test1) |
| ofac | `0.2.4-candidate` | [cntr-rpa-ofac-0.2.4-test30](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ofac-0.2.4-test30) |
| senescyt | `0.1.5-candidate` | [cntr-rpa-senescyt-0.1.5-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-senescyt-0.1.5-test1) |
| sercop | `0.1.1-candidate` | [cntr-rpa-sercop-0.1.1-test31](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sercop-0.1.1-test31) |
| servicios_educacion | `0.1.2-candidate` | [cntr-rpa-servicios-educacion-0.1.2-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-servicios-educacion-0.1.2-test1) |
| sri | `0.1.24-candidate` | [cntr-rpa-sri-0.1.24-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.24-test1) |
| supercias | `0.1.22-candidate` | [cntr-rpa-supercias-0.1.22-test1](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.22-test1) |

C.197 incorpora `supercias@0.1.19-candidate` sin cambiar motor ni los otros adaptadores. Reconoce el aviso concluyente de RUC inexistente como `NO_MATCH` con evidencia por documento; la corrida integrada TEST 1966 confirmó tres archivos y tres ACK para ese caso, junto con tres PDFs y tres ACK de una compañía existente. El ZIP firmado se verificó con descarga pública HTTP 200 y SHA-256 correcto.

C.156 actualiza `servicios_educacion@0.1.2-candidate` y `senescyt@0.1.3-candidate` como candidatos TEST firmados. Estas revisiones usan únicamente la fachada pública `PortalActions` del motor. SENESCYT recupera una sesión JSF vencida y limpia el formulario al cambiar de sujeto en la misma pestaña. La publicación del canal no activa documentos ni acredita por sí sola evidencia o ACK desde el robot. El motor permanece en la versión indicada y no se recompiló por estos adaptadores.

La asignación efectiva de cada documento sigue siendo la versión que entregue ORDS. INTERPOL conserva su barrera de autorización para consultas externas.

C.178 incorpora en TEST `consejo_judicatura@0.1.8-candidate` y `lista_clinton@0.1.5-candidate`, con URL propia validada por aplicación y sin depender de `work.entry_url`. El motor TEST sigue en `1.0.24-test.1`; el canal de Producción conserva `1.0.24`. ORDS asigna actualmente el documento 33 a `ofac`; Lista Clinton no se asigna ni se promueve a Producción por esta tarea.

C.157 publica el motor `1.0.11-test.1` y Supercias `0.1.17-candidate`: resultado individual por sujeto, continuidad tras timeout y prioridad PDF `RL → ADM` para el documento 16. La generación 89 es un candidato de TEST; su firma y disponibilidad pública no sustituyen la prueba instalada con evidencia y ACK.

La generación 90 sustituye solamente SENESCYT por `0.1.4-candidate`. La aplicación comprueba que la identificación permanezca tras la recarga JSF tardía y la repone antes de continuar con el CAPTCHA. La instalación TEST con dos sujetos y evidencia/ACK se comprueba por separado.

C.159 publica como candidatos TEST el motor `1.0.14-test.1` y Ministerio `0.1.7-candidate`. El primero recupera solo la pestaña tras timeout; el segundo vincula checkpoint y PDF al sujeto actual. La generación 95 está firmada; su integración real y el pase productivo quedan sujetos al expediente C.159, sin inferirse del código o de los fixtures locales.

## Engine 1.0.25 TEST — generación 110

Publicación firmada del ejecutable 1.0.25 desde RPA commit 3bad69a37714de6f6c7596ca5e1c5f8575905e5b; conserva las 12 asignaciones de adaptadores de generación 109 e incluye Ministerio del Interior 0.1.9-candidate. La validación de la aplicación del portal con dos sujetos terminó MATCH y generó evidencia para ambos. El paso de actualización instalada se documenta tras completar la prueba del actualizador.

## C.189 — Superintendencia 0.1.18 TEST

La generación 111 incorpora `supercias@0.1.18-candidate` desde RPA commit `a153ff51052ba6faf3e69ca4edb773e279ddcfd7`; conserva el motor `1.0.25-test.1` y las demás asignaciones. El candidato reutiliza la ficha por sujeto para los documentos 17–19. El QA real de TEST confirmó los tres documentos con PDF y ACK en una sesión; el expediente privado de la tarea conserva el detalle de ejecución y cotejo de hashes. Esta publicación TEST no cambia el canal PRODUCCIÓN ni certifica otros documentos o configuraciones.


C.199 incorpora `supercias@0.1.20-candidate` para el documento 19. La corrida integrada TEST 2008 / detalle 2722 terminó `COMPLETADO`, con ACK `ACKED` y un único PDF de 16 páginas que contiene los ejercicios 2025 y 2024. El paquete firmado se generó desde el commit RPA `65ab74bc7b252c031785cdab89dec4d1c48c0103`; su asset público se verificó por tamaño y SHA-256. El motor y los otros adaptadores no cambian.