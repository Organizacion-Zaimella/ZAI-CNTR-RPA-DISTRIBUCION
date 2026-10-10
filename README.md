# CNTR RPA — distribución pública

Repositorio de distribución de software aprobado del proyecto CNTR RPA, propiedad de **Organizacion-Zaimella**. La descarga pública está prevista para clientes sin cuenta, token ni sesión de GitHub. El código en desarrollo, los datos operativos y las configuraciones permanecen en sus fuentes privadas.

**Estado actual de esta rama de prueba:** canal firmado TEST generación 18, motor `1.0.0-test.7` y seis adaptadores candidatos, incluido OFAC `0.1.4-candidate` en [`cntr-rpa-ofac-0.1.4-test1`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-ofac-0.1.4-test1). Los módulos siguen siendo candidatos de QA, **no están certificados ni aprobados para Producción**. Esta rama no modifica `main`; las pruebas de descarga usan un sandbox Windows aislado.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Reporte privado de seguridad](SECURITY.md)

El acceso de lectura del repositorio es anónimo. Los assets TEST llevan firma y hashes; el canal TEST no se debe confundir con certificación funcional ni con aprobación de Producción. No se alojan datos de sujetos, documentos, evidencias ni secretos.
