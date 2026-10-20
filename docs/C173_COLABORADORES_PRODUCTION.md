# C.173 — motor 1.0.21 en Producción

El motor 1.0.21 procede del commit RPA
`7f1456d47cb28d0f4611252cfdffcf13a8ae4441`, integrado en `main`.
La generación TEST 103 firmada publicó `1.0.21-test.1`. El promotor descargó
su asset público, verificó tamaño, hash y firma, y extrajo el mismo EXE para
firmarlo en el canal PRODUCCIÓN generación 21. Los adaptadores y revocaciones
de la generación 20 permanecen idénticos.

QA dirigido en TEST: configuración 865 con 556 sujetos y siete documentos
activos; ORDS entregó 3.892 parejas y el contrato del motor validó las 3.892.
El EXE aislado 1.0.21 pasó el preflight de adaptadores firmados y
`--check-ords` con 31 configuraciones y 3.969 parejas, `plan=OK`. La
regresión local del motor y actualizador pasó con 102 pruebas aprobadas y
cuatro omitidas; el build del EXE pasó su gate `V100_BUILD_PASS`.

El usuario obtiene el motor nuevo en el próximo inicio normal del launcher
firmado; no requiere reinstalar. El resultado real de la siguiente corrida
productiva se observará por cabecera, detalle, evidencias y ACK. No se hizo
una corrida funcional en Producción durante el pase.
