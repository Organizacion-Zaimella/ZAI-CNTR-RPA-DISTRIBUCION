# CNTR RPA — distribución pública

Repositorio de distribución de software aprobado del proyecto CNTR RPA, propiedad de **Organizacion-Zaimella**. La descarga pública está prevista para clientes sin cuenta, token ni sesión de GitHub. El código en desarrollo, los datos operativos y las configuraciones permanecen en sus fuentes privadas.

**Rama candidata TEST:** prerelease firmado [`cntr-rpa-1.0.0-test.11`](https://github.com/Organizacion-Zaimella/ZAI-CNTR-RPA-DISTRIBUCION/releases/tag/cntr-rpa-1.0.0-test.11), canal generación 9, motor `1.0.0-test.5` y adaptadores IESS `0.1.3-candidate`, OFAC `0.1.1-candidate` y SRI `0.1.2-candidate`. Son candidatos de QA, **no módulos certificados ni una distribución de Producción**. IESS reutiliza la misma aplicación independiente para la adquisición y validación de PDF. La rama `main` no se modifica; ORDS aún fija IESS a `0.1.0-candidate`.

- [Arquitectura de distribución](docs/ARQUITECTURA_DISTRIBUCION.md)
- [Publicación y aprobación](docs/PUBLICACION.md)
- [Uso desde el RPA](docs/USO_DESDE_RPA.md)
- [Reporte privado de seguridad](SECURITY.md)

El acceso de lectura del repositorio es anónimo. Los assets TEST llevan firma y hashes; el canal TEST no se debe confundir con certificación funcional ni con aprobación de Producción. No se alojan datos de sujetos, documentos, evidencias ni secretos.
