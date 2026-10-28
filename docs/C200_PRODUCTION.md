# C.200 — SRI 0.1.24 y Supercias 0.1.21 en Producción

Publicación preparada por solicitud expresa del usuario para validar contra el portal en Producción cuando vuelva a estar disponible.

- Fuente RPA integrada: `2742dd47a263ad83c5c9874d9c610f53d321631e`.
- Canal previo: generación 31, motor `1.0.27`; nuevo canal: generación 32. Motor, revocaciones y adaptadores distintos de SRI/Supercias se preservan.
- SRI: `sri@0.1.24`, release [`cntr-rpa-sri-0.1.24`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-sri-0.1.24), SHA-256 `9a3e64964ca00854223114f14677c6f2560288b8038ed686261d7951c3d28f33`.
- Supercias: `supercias@0.1.21`, release [`cntr-rpa-supercias-0.1.21`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-supercias-0.1.21), SHA-256 `0536d9ae08881c2e91959a5e82a1fc61f8945f75022f833fb7a309ac449586d7`.
- Firmas: raíz de Producción `cntr-prod-63f2371d344a`; canal SHA-256 `a5f7996c3f505d9f0f82e6adcef7b91e4a848d94b947152018b0d6a58c2d6b6e`.
- Los assets estables se descargaron anónimamente por HTTPS (HTTP 200); tamaño y SHA-256 coinciden con el canal firmado.
- Suite local de SRI/Supercias: 74 aprobadas. QA integrado TEST no se completó: 6/14 pares validados antes de que el portal bloqueara temporalmente la consulta. La publicación no certifica el flujo integral. El usuario hará validación productiva cuando se habilite el portal.
- Tras integrar el PR de canal, el launcher instalado recibe las versiones nuevas al iniciar; no requiere reinstalación. Verificar en la primera corrida visible el canal/generación, motor y versiones, y contrastar evidencias/ACK de SRI y documentos Supercias.
