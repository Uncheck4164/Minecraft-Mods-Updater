import urllib.request
import zipfile
import os
from tqdm import tqdm
import requests
import subprocess
#Sorry futuro yo o persona que lea esto por el desorden xd

def pregunta_ruta():
    print("\033[4;31m"+"IMPORTANTE SE BORRARAN TODOS TUS ARCHIVOS DE .MINECRAFT/MODS"+ "\033[0m")
    pregunta = input("¿Has editado la ruta de tu .minecraft? 1.Sí 2.No: ")
    while not pregunta.isdigit() or int(pregunta) not in [1, 2]:
        pregunta = input("Por favor, ingresa una opción válida (1 o 2): ")
    return int(pregunta)

def ruta_minecraft(preguntaRuta):
    ruta_minecraft = os.path.join(os.environ['APPDATA'], '.minecraft')

    if not os.path.exists(ruta_minecraft) and preguntaRuta == 2:
        print("La ruta de .Minecraft no existe. Verifica la ruta.")
        print("""
            Lista de posibles errores
            -No has abierto Minecraft
            -Tienes .Minecraft en otro disco duro o ubicación, sí es el caso seleccione opción 1
            -No has instalado Minecraft
            ¿Cómo verificarlo?
            Presione -tecla Windows-
            escriba %APPDATA%
            Verifique que exista .Minecraft
            Si existe comuniquese conmigo por Discord: nadie#1565  
        """)
        return None
    if (preguntaRuta == 1 and os.path.exists(ruta_minecraft)) or not os.path.exists(ruta_minecraft):
        print("\033[91mTu .minecraft se detectada correctamente ¿seguro quieres continuar? si no cierra y vuelve abrir\033[0m")
        while preguntaRuta == 1:
            ruta_minecraft = input("Introduce la ruta de una carpeta atras de .minecraft, ejemplo C:/Users/AppData/Roaming: ")

            if os.path.exists(os.path.join(ruta_minecraft, ".minecraft")):
                print(".minecraft existe en la ruta:", os.path.join(ruta_minecraft, ".minecraft"))
                preguntaRuta = None
                ruta_minecraft = os.path.join(ruta_minecraft, ".minecraft")
            else:
                print(".minecraft no existe en la ruta:", os.path.join(ruta_minecraft, ".minecraft"))
    return ruta_minecraft

def verificar_forge(rutaMinecraft,minecraftVersion,forgeVersion):

    forge_dir = os.path.join(rutaMinecraft, 'versions', f'{minecraftVersion}-forge-{forgeVersion}')
    if not os.path.isdir(forge_dir):
        print(f"\033[4;31mForge no está instalado para Minecraft {minecraftVersion}. O hubo una actualización.\033[0m")
        return None
    print(f"Forge está instalado en la carpeta: {forge_dir}")
    return True
def descargar_forge(minecraftVersion,forgeVersion,rutaMods):
    # Preguntar al usuario si desea instalar Forge
    respuesta = input("¿Desea instalar Forge? (s/n)")
    if respuesta.lower() == "s":
        url = f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{minecraftVersion}-{forgeVersion}/forge-{minecraftVersion}-{forgeVersion}-installer.jar"
        nombre_archivo = f"forge-{minecraftVersion}-{forgeVersion}-installer.jar"
        ruta_descarga = os.path.join(os.getcwd(), nombre_archivo)
    
        print("\033[32m" + f"Descargando {nombre_archivo} desde {url}" + "\033[0m")
        respuesta = requests.get(url)
    
        with open(ruta_descarga, "wb") as archivo:
            archivo.write(respuesta.content)
    
        print("\033[0;32m"+"Descarga completa!"+ "\033[0m")
    
        print("\033[0;32m"+"Instalando "+nombre_archivo+"..."+ "\033[0m")
        subprocess.call(["java", "-jar", ruta_descarga])
        # Eliminar el instalador de Forge
        os.remove(f"forge-{minecraftVersion}-{forgeVersion}-installer.jar")
        os.remove("installer.log")
        return True
    else:
        print("\033[91m" + "No se ha instalado Forge." + "\033[0m")
        return False

def descargar_archivo(urlArchivo, nombreArchivo, rutaDestino):
    """
    Descarga el archivo desde la URL y lo guarda en la ruta especificada.
    url_archivo: str - La URL del archivo a descargar.
    nombre_archivo: str - El nombre del archivo que se guardará en la ruta especificada.
    ruta_destino: str - La ruta donde se guardará el archivo descargado.
    """
    with tqdm(unit="B", unit_scale=True, unit_divisor=1024) as t:
        urllib.request.urlretrieve(urlArchivo, f"{rutaDestino}/{nombreArchivo}", 
                                   reporthook=lambda blocknum, blocksize, totalsize: t.update(blocksize))
    zip_file = zipfile.ZipFile(f"{rutaDestino}/{nombreArchivo}", 'r')
    with tqdm(total=len(zip_file.namelist()), unit='file', unit_scale=True, unit_divisor=1024, miniters=1,
              desc='Extrayendo archivo') as t:
        for archivo in zip_file.namelist():
            zip_file.extract(archivo, rutaDestino)
            t.update()
    zip_file.close()
    os.remove(f"{rutaDestino}/{nombreArchivo}")

def verificar_version(urlVersion,rutaMods):
    """
    Compara la versión actual con la versión anterior, si existe.
    url_version: str - La URL del archivo de versión.
    ruta_version: str - La ruta donde se encuentra el archivo de versión.
    """
    
    with urllib.request.urlopen(urlVersion) as f:
        version_actual = f.read().decode("utf-8").strip()
    try:
        with open(f"{rutaMods}/version.txt", "r") as f:
            version_anterior = f.read().strip()
    except FileNotFoundError:
        version_anterior = None
    if version_anterior == version_actual:
        print("No hay actualización disponible.")
        print(f"Tu versión actual es v{version_actual}")
    else:
        descargar_archivo(url_archivo, "mods.zip", rutaMods)
        print("Se ha descargado la nueva versión.")
        print(f"Actualizacion de v{version_anterior} a v{version_actual}")
        # Guardar la nueva versión en el archivo version.txt
        with open(f"{rutaMods}/version.txt", "w") as f:
            f.write(version_actual)

def mc_forge_version(ruta,minecraft_forge):
    ruta_local = f'{ruta}/minecraft_forge.txt'
    urllib.request.urlretrieve(minecraft_forge, ruta_local)

    with open(ruta_local, 'r') as archivo:
        datos = archivo.readlines()

    minecraft_version = datos[0].strip()
    forge_version = datos[1].strip()

    return minecraft_version, forge_version

def crear_carpeta_mods(rutaMods):
    if not os.path.exists(rutaMods):
        os.mkdir(rutaMods)
        print("La carpeta '{}' ha sido creada en la ruta '{}'.".format("mods", rutaMods))
    else:
        print("Okey..")
     
url_version = ""
url_archivo = ""
minecraft_forge = ""

ruta = ruta_minecraft(pregunta_ruta())
ruta_mods = os.path.join(ruta, 'mods')
minecraft_version, forge_version = mc_forge_version(ruta,minecraft_forge)

forge = verificar_forge(ruta,minecraft_version,forge_version)
if not forge:
    descargar_forge(minecraft_version,forge_version,ruta_mods)
if not os.path.exists(os.path.join(ruta, 'versions', f'{minecraft_version}-forge-{forge_version}')):
    print("\033[31m"+"No se puede continuar sin forge. Si lo descarga y no funciona, comuníquese conmigo nadie#1565." + "\033[0m")
    os.system("pause")
    exit()
print("\033[0;32m"+"¡Instalación completa!"+ "\033[0m")

crear_carpeta_mods(ruta_mods)

verificar_version(url_version,ruta_mods)
