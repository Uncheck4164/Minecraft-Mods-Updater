# ¿Qué hace?
Este script permite descargar e instalar mods en Minecraft desde la nube, lo que facilita enormemente el proceso de jugar con amigos y actualizar Minecraft, Forge o los mods. Lee una ruta de configuración desde un archivo JSON y verifica si el usuario tiene instalado Minecraft Forge; si no lo tiene, lo descarga e instala automáticamente. Luego descomprime el archivo del mod en la carpeta correspondiente de mods de Minecraft.

# Como instalarlo
Instalar la dependencia con el siguiente comando:
```
pip install tqdm
pip install requests
 ```

Rellenar las variables `url_version` y `minecraft_forge` con los enlaces de los archivos `version.txt` y `minecraft_forge.txt` respectivamente. Estos archivos deben estar alojados en la nube o en un servidor. Las variables quedarían así:

- url_version = "https://yourhost/version.txt"
- minecraft_forge = "https://yourhost/minecraft_forge.txt"

Agregar el archivo `.zip` con los mods, que debe llamarse `mods.zip`, de la siguiente manera:
- url_archivo = "https://yourhostcom/mods.zip"

En el archivo `version.txt`, agregar la versión del programa. Por ejemplo:
- 1.0
Esto debe ser modificado cada vez que se quieran actualizar los mods.

En el archivo `minecraft_forge.txt`, agregar la versión de Minecraft y la de Forge, separadas por un espacio. Por ejemplo:
- 1.19.3
- 44.1.0

Para convertir el archivo a un ejecutable `.exe`, se puede utilizar la herramienta `auto-py-to-exe`. Una vez hecho esto, el programa está listo para ser utilizado.

**Dato importante**:
Este script fue diseñado para mi uso personal y, aunque aún estoy aprendiendo, si alguien más puede beneficiarse de él, me alegra mucho 🫡. Actualmente, el programa se limita a añadir los `mods` a la carpeta correspondiente en la PC del usuario, sin instalarlos ni llevar a cabo ninguna otra acción, y solo es compatible con Forge. Ha sido probado únicamente en Windows y no se ha profundizado en su funcionamiento en otros sistemas operativos. El único objetivo de este pequeño programa es descargar el archivo `.zip` y descomprimirlo en la carpeta `mods`. En el futuro, se podrían añadir más funcionalidades al código para mejorar su utilidad.

Es posible que existan algunos bugs en el programa, ya que solo puedo desarrollar por las noches y puede que esté un poco cansado. Si encuentra algún error, por favor comuníquese conmigo en nadie#1565.