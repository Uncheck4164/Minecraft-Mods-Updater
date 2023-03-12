# ¿Cómo ejecutarlo?

Instalamos la dependencia:

```$ pip install tqdm```


Añadimos a las variables el enlace de 2 archivos .txt, estos deben estar en la nube/hosting:

version.txt
minecraft_forge.txt
Quedaría como:
-url_version = "https://yourhost.000webhostapp.com/version.txt"
-minecraft_forge = "https://yourhost.000webhostapp.com/minecraft_forge.txt"

Además, también añadimos el archivo .zip, el cual tiene que llamarse "mods.zip". Quedaría como:
-url_archivo = "https://yourhost.000webhostapp.com/mods.zip"

Dentro de "version" tienes que añadir la versión del programa. Ejemplo: 1.0. Esto debe ser modificado cada vez que se quieran actualizar los mods.

Y en "minecraft_forge" va la versión de Minecraft y la de Forge, estas tienen que ir con un espaciado. Ejemplo:
-1.19.3
-44.1.0

Luego, para convertirlo a un archivo .exe puedes utilizar auto-py-to-exe. Y con eso, ya queda listo para su uso 👌.

**Dato importante**:
esto solo añade mods a la carpeta "mods" de la PC de alguien. Solo fue testeado en Windows y no profundicé sobre otros sistemas operativos. Lo único que hace este pequeño script es descargar el .zip y descomprimirlo en la carpeta "mods", nada más (podría modificar este código en el futuro para hacer más funciones).