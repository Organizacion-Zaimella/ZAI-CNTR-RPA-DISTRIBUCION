# C.200 — Supercias 0.1.24 en Producción

El canal firmado de Producción generación 33 actualiza exclusivamente Supercias a `0.1.24`. El motor `1.0.27`, los demás adaptadores y las revocaciones se conservan.

- Fuente RPA integrada: `694d4735147db0c7f3eb782115604ef5e059e1c4`; los archivos Supercias coinciden con la fuente usada en TEST `8cfd9f307c3fd063726dddffe67762904f219f25`.
- TEST 2037: dos sujetos y siete documentos cada uno; 13 detalles `COMPLETADO` con PDF y uno `SIN_RESULTADO` con captura, 14 evidencias y ACK. Los dos balances incluyen 2025 y 2024. Suite Supercias: 51 pruebas aprobadas.
- [Release estable cntr-rpa-supercias-0.1.24](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.24); ZIP SHA-256 `faca1381a44677d00966a371f9e59830da3e04d8bffd2caaa1795e873df970ee`. ZIP, manifiesto, firma y SBOM verificados mediante descargas públicas HTTP 200 y hashes.
- Canal firmado con la raíz `cntr-prod-63f2371d344a`, SHA-256 `9968da695b97af36ae5a1a6cc505faa0e0d95bdd807bcbb81a41a374124d9e61`. La actualización se recibe al iniciar el launcher ya instalado.
- Actualizador probado en instalación aislada con el canal propuesto firmado: verificó y activó motor `1.0.27` y adaptador `0.1.24`, descargando el manifiesto y el ZIP públicos y superando el autocontrol del motor.
- La prueba documental usó motor 1.0.27 y la fuente candidata en una instalación temporal; el canal TEST firmado fue publicado y verificado posteriormente. No se hizo una corrida documental en Producción.
