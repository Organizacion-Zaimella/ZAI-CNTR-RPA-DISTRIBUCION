# C.153 — Canal firmado y continuidad

La versión ejecutable del motor y cada adaptador procede exclusivamente del canal firmado del ambiente. ORDS conserva la autoridad sobre configuración, elegibilidad, sujetos, documentos, orden y función. El número de versión de adaptador enviado por ORDS es una referencia heredada y puede quedar atrasado; el motor usa la versión compatible y firmada, y registra la diferencia sin datos personales.

Una versión de adaptador no presente en el canal no se descarga ni se ejecuta. El motor debe registrar el trabajo afectado como reintentable por fallo técnico y continuar el siguiente del plan, conservando journal, evidencia y ACK. La publicación en GitHub no constituye certificación documental.

Antes de promover el canal, una sesión HTTP anónima, sin token ni cookies, debe comprobar HTTP 200 y hash exacto para cada asset nombrado en el Release: `release-manifest.json`, `release-manifest.json.sig` y ZIP. Después se comprueban firmas de Release y canal, compatibilidad, revocaciones y ejecución instalada. Una ausencia del manifiesto genérico impide promover el canal aunque exista un archivo con prefijo de versión.

Motor 1.0.5: fuente RPA `9d6a352a1db475dbb5fe0a82986891e2b61fb419`; Release `cntr-rpa-engine-1.0.5`; canal propuesto generación 7. Los tres assets del Release devolvieron HTTP 200 anónimo y sus SHA-256 coincidieron con los firmados antes de esta propuesta. La activación y la prueba instalada requieren el merge de este canal.
