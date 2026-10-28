# C.200 — candidatos TEST SRI y Supercias

- Fuente RPA integrada en `main`: `2742dd47a263ad83c5c9874d9c610f53d321631e` (SRI) y candidato `bfbc395d14d66f9857451fb5dd9645411b85a343` (reintento acotado de navegación inicial Supercias).
- SRI `0.1.24-candidate`: release `cntr-rpa-sri-0.1.24-test1`.
- Supercias `0.1.23-candidate`: release `cntr-rpa-supercias-0.1.23-test1`.
- Canal TEST: generación 120; conserva motor `1.0.28-test.1` y el resto de asignaciones.
- Supercias pasó 50 pruebas locales. La corrida integrada previa confirmó 13 de 14 pares (docs. 13–19 para dos empresas); el único pendiente fue la navegación inicial del doc. 17. El candidato 0.1.23 agrega un reintento acotado y checkpoints privados de esa fase. La verificación ORDS de ese par continúa pendiente; la publicación TEST no certifica aún ese flujo.
- No se promueve a Producción desde este expediente hasta completar la verificación integrada TEST y el gate autorizado correspondiente.
