# C.173 — motor 1.0.21 en TEST

El motor del commit RPA `7f1456d47cb28d0f4611252cfdffcf13a8ae4441` se
distribuye como `1.0.21-test.1` en la generación TEST 103. El asset y los
manifiestos usan la clave de firma TEST. Los 12 adaptadores y la lista de
revocación conservan sus asignaciones anteriores.

La configuración de QA 865 replica las 556 asociaciones de sujetos y los
nueve documentos de la configuración productiva 321, de los cuales siete están
activos. No se copiaron evidencias ni historial. El motor 1.0.21 leyó desde
ORDS TEST las 3.892 parejas pendientes, validó su contrato y completó el
preflight firmado. La consulta integral con el EXE aislado reportó 31
configuraciones, 3.969 parejas y `plan=OK`. Datos personales, OAuth y
payload de migración permanecen fuera de Git.

La prueba acredita la corrección del arranque y la paginación. La ejecución de
los documentos ante portales externos se conserva como observación posterior
del usuario; el cambio C.173 no modifica adaptadores.
