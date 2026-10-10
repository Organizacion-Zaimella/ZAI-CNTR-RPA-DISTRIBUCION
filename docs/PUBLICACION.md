# Política de publicación

1. Desarrollar y revisar cambios en su repositorio fuente, registrando commit y pruebas.
2. Revisar contenido publicable: datos personales, evidencias, cookies, URLs internas y claves privadas no se incluyen.
3. Construir desde fuente versionada con dependencias bloqueadas y SBOM; firmar manifest y artefactos con una clave custodiada fuera del repositorio.
4. Publicar assets como releases inmutables; nunca sobrescribir tags ni assets.
5. Promover un candidato a un puntero del canal correspondiente solo tras sus gates. Un canal TEST no autoriza Producción.
6. Registrar revocación, rollback, commit fuente, firma y SHA-256.

Las ramas de prueba no modifican `main` ni el canal Producción. La existencia de un candidato no equivale a certificación para Producción.
