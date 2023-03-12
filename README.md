# ¿Cómo ejecutarlo?

Instalar la dependencia con el siguiente comando:
```
pip install tqdm
 ```

Rellenar las variables `url_version` y `minecraft_forge` con los enlaces de los archivos `version.txt` y `minecraft_forge.txt` respectivamente. Estos archivos deben estar alojados en la nube o en un servidor. Las variables quedarían así:

- url_version = "https://yourhost.000webhostapp.com/version.txt"
- minecraft_forge = "https://yourhost.000webhostapp.com/minecraft_forge.txt"

Agregar el archivo `.zip` con los mods, que debe llamarse `mods.zip`, de la siguiente manera:
- url_archivo = "https://yourhost.000webhostapp.com/mods.zip"

En el archivo `version.txt`, agregar la versión del programa. Por ejemplo:
- 1.0
Esto debe ser modificado cada vez que se quieran actualizar los mods.

En el archivo `minecraft_forge.txt`, agregar la versión de Minecraft y la de Forge, separadas por un espacio. Por ejemplo:
- 1.19.3
- 44.1.0

Para convertir el archivo a un ejecutable `.exe`, se puede utilizar la herramienta `auto-py-to-exe`. Una vez hecho esto, el programa está listo para ser utilizado.

**Dato importante**:
Este script solo añade los `mods` a la carpeta mods de la PC del usuario. Ha sido probado únicamente en Windows y no se ha profundizado sobre su funcionamiento en otros sistemas operativos. El único objetivo de este pequeño programa es descargar el archivo `.zip` y descomprimirlo en la carpeta `mods`, nada más. (En el futuro, se podrían añadir más funcionalidades al código).
