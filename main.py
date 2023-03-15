import urllib.request
import zipfile
import os
from tqdm import tqdm
import requests
import subprocess
import json
import time
# Rellenar variables con urls de hosting/nube
with open("config.json") as f:
    config = json.load(f)


url_version = config["url_version"]
url_archivo = config["url_archivo"]
minecraft_forge = config["minecraft_forge"]

def pregunta_ruta():
    print("\033[4;31m"+"IMPORTANTE SE BORRARAN TODOS TUS ARCHIVOS DE .MINECRAFT/MODS"+ "\033[0m")
    print("\033[31m"+"En caso de error hablame nadie#1565"+ "\033[0m")
    pregunta = input("¿Has editado la ruta de tu .minecraft? (yes/no)").lower()
    if pregunta != "yes" and pregunta!= "no":
        pregunta_ruta()
    ruta = ruta_minecraft(pregunta)
    os.system("cls")
    if ruta == None:
        pregunta_ruta()
        ruta = os.path.join(os.environ['APPDATA'], '.minecraft')
    return ruta

def ruta_minecraft(respuestaRuta):
    ruta_minecraft = os.path.join(os.environ['APPDATA'], '.minecraft')

    if not os.path.exists(ruta_minecraft) and respuestaRuta == "no":
        print("La ruta de .Minecraft no existe. Verifica la ruta.")
        print("""
            Lista de posibles errores:
            - No has abierto Minecraft.
            - Tienes .Minecraft en otro disco duro o ubicación; si es el caso, selecciona la opción 1.
            - No has instalado Minecraft.

            ¿Cómo verificarlo?
            Presiona la tecla Windows.
            Escribe %APPDATA%.
            Verifica que exista .Minecraft.
        """)
        os.system("pause")
        pregunta_ruta()
    
    if not (respuestaRuta == "yes" and os.path.exists(ruta_minecraft)):
        return
    
    respuesta_confirmacion = input("\033[31m.minecraft se ha detectado correctamente. ¿Estás seguro de que quieres continuar? (yes/no) \033[0m").lower()
    if respuesta_confirmacion == "no":
        return
    
    incorrect_path = True
    while incorrect_path:
        ruta_minecraft = input("Introduce la ruta de la carpeta .minecraft, por ejemplo, C:/Users/AppData/Roaming/.minecraft: ")
        ruta_minecraft = os.path.normpath(ruta_minecraft)
    
        if not os.path.exists(os.path.join(os.path.dirname(ruta_minecraft), ".minecraft")):
            os.system("cls")
            print("\033[31m.minecraft no se ha encontrado en la ruta proporcionada:", ruta_minecraft, "\033[0m")
            continue
        
        print("\033[32m.minecraft se ha detectado correctamente en la ruta:", ruta_minecraft, "\033[0m")
        incorrect_path = False    
       
    return ruta_minecraft

def verificar_forge(rutaMinecraft,minecraftVersion,forgeVersion):

    forge_dir = os.path.join(rutaMinecraft, 'versions', f'{minecraftVersion}-forge-{forgeVersion}')
    if not os.path.isdir(forge_dir):
        print(f"\033[4;31mForge no está instalado para Minecraft {minecraftVersion}. O hubo una actualización.\033[0m")
        return
    print(f"\033[33mForge está instalado en la carpeta: {forge_dir}\033[0m")
    time.sleep(1.3)
    return True

def find_java():
    java_path = None
    if os.name == 'nt':  # Windows
        print("Windows")
        time.sleep(0.7)
        try:
            # Intenta obtener la variable de entorno JAVA_HOME
            java_home = os.environ['JAVA_HOME']
            if os.path.exists(java_home):
                # Busque el ejecutable java en el directorio JAVA_HOME
                java_path = os.path.join(java_home, 'bin', 'java.exe')
        except KeyError:
            # Si la variable de entorno JAVA_HOME no está configurada, busque java en la RUTA
            for path in os.environ['PATH'].split(os.pathsep):
                java_path = os.path.join(path, 'java.exe')
                if os.path.exists(java_path):
                    break
        if not java_path:
            raise Exception('No se encontró una instalación de Java en el sistema.')
    else:  # Unix-based system
        print("Unix o MacOs")
        time.sleep(1.2)
        try:
            subprocess.check_output(['which', 'java'])
            java_path = 'java'
        except subprocess.CalledProcessError:
            raise Exception('No se encontró una instalación de Java en el sistema.')
    return java_path

def descargar_forge(minecraftVersion,forgeVersion,ruta):
    # Preguntar al usuario si desea instalar Forge
    respuesta = input("¿Desea instalar Forge? (s/n)")
    if respuesta.lower() != "s":
        print("\033[91m" + "No se ha instalado Forge." + "\033[0m")
        return False
     
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
    print("\033[0;32m"+"¡Instalación completa!"+ "\033[0m")
    time.sleep(1.3) 
    return True
        
def descargar_archivo(urlArchivo, nombreArchivo, rutaMods):
    """
    Elimina los archivos de la carpeta mods
    Descarga el archivo desde la URL y lo guarda en la ruta especificada.
    url_archivo: str - La URL del archivo a descargar.
    nombre_archivo: str - El nombre del archivo que se guardará en la ruta especificada.
    ruta_destino: str - La ruta donde se guardará el archivo descargado.
    """
    for archivo in os.listdir(rutaMods):
        archivo_path = os.path.join(rutaMods, archivo)
        if os.path.isfile(archivo_path):
            os.remove(archivo_path)
    
    # Desca archivo mods.zip
    with tqdm(unit="B", unit_scale=True, unit_divisor=1024) as t:
        urllib.request.urlretrieve(urlArchivo, f"{rutaMods}/{nombreArchivo}", 
                                   reporthook=lambda blocknum, blocksize, totalsize: t.update(blocksize))
    # Descomprime mods.zip    
    zip_file = zipfile.ZipFile(f"{rutaMods}/{nombreArchivo}", 'r')
    with tqdm(total=len(zip_file.namelist()), unit='file', unit_scale=True, unit_divisor=1024, miniters=1,
              desc='Extrayendo archivo') as t:
        for archivo in zip_file.namelist():
            zip_file.extract(archivo, rutaMods)
            t.update()
    zip_file.close()
    # Borra mods.zip
    os.remove(f"{rutaMods}/{nombreArchivo}")

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
        os.system("cls")
        print("\033[34mNo hay actualización disponible.\033[0m")
        print(f"\033[34mTu versión actual es v{version_actual}\033[0m")

        os.system("pause")
    else:
        descargar_archivo(url_archivo, "mods.zip", rutaMods)
        os.system("cls")
        print("\033[35mSe ha descargado la nueva versión.\033[0m")
        print(f"\033[35mActualizacion de v{version_anterior} a v{version_actual}\033[0m")

        # Guardar la nueva versión en el archivo version.txt
        with open(f"{rutaMods}/version.txt", "w") as f:
            f.write(version_actual)
        os.system("pause")
        
def mc_and_forge_version(ruta,minecraftForge):
    ruta_local = f'{ruta}/minecraft_forge.txt'
    urllib.request.urlretrieve(minecraftForge, ruta_local)

    with open(ruta_local, 'r') as archivo:
        datos = archivo.readlines()

    minecraft_version = datos[0].strip()
    forge_version = datos[1].strip()
    app_version = datos[2].strip()

    return minecraft_version, forge_version, app_version

def crear_carpeta_mods(rutaMods):
    if not os.path.exists(rutaMods):
        os.mkdir(rutaMods)
        print("La carpeta '{}' ha sido creada en la ruta '{}'.".format("mods", rutaMods))
        time.sleep(1.3)
    else:
        print("\033[32mOkey\033[0m...")
        time.sleep(1.2)
    
def update_app():
    ruta_local = f'{ruta}/minecraft_forge.txt'

    with open(ruta_local, 'r') as archivo:
        datos = archivo.readlines()

ruta = pregunta_ruta()
ruta_mods = os.path.join(ruta, 'mods')
minecraft_version, forge_version, app_version = mc_and_forge_version(ruta,minecraft_forge)
print(f"V{app_version} App")
time.sleep(1)
os.system("cls")
find_java()
forge = verificar_forge(ruta,minecraft_version,forge_version)

if not forge:
    descargar_forge(minecraft_version,forge_version,ruta)
if not os.path.exists(os.path.join(ruta, 'versions', f'{minecraft_version}-forge-{forge_version}')):
    print("\033[31m"+"No se puede continuar sin forge. Si lo descarga y no funciona, comuníquese conmigo nadie#1565." + "\033[0m")
    os.system("pause")
    exit()

crear_carpeta_mods(ruta_mods)
verificar_version(url_version,ruta_mods)
