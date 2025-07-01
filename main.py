import os
import json
from logs.logs import logger, error_logger
from dotenv import load_dotenv
from pages.login_sura import login_sura
import requests



# Ruta al archivo config.json (ajusta según tu estructura)
config_path = os.path.join(os.path.dirname(__file__), "config", "params.json")
logger.info(f"Ruta del archivo de parametros: {config_path}")

# Leer el archivo JSON
with open(config_path, "r", encoding="utf-8") as f:
    config_data = json.load(f)

# Extraer las variables
paths = config_data["paths"][0]
url_sura = paths["strUrlSura"]
url_actualizar_token = paths["strUrlActualizarToken"]
logger.info(f"Variables obtenidas url pagina sura: {url_sura}, endPoint del token {url_actualizar_token}")


#cargar el archivo env y llamar las variables
load_dotenv()
usuario_sura            = os.getenv("USUARIO")
contrasenia_sura        = os.getenv("CONTRASENIA")



#Llamar el loguin para obtener la cookies de inicio de ssesion
token = login_sura(usuario_sura, contrasenia_sura, url_sura)
logger.info(f"Token de acceso: {token}")

#Validar acceso y actualizar token
if token:

    # Hacemos la petición POST para actualizar el token
    response = requests.post(url_actualizar_token, json=token)
    logger.info(f"Respuesta actualizacion del token de acceso: {response}")

    #Validar respuesta de la actualizacion del token
    if response.status_code == 200:
        logger.info(f"{response.json()["mensaje"]}: estatus {response.status_code}")
    else:
        error_logger.error(f"Hubo un error actualizando el token: {response}")

else:
    error_logger.error(f"Hubo un error ingresando a sura revise las credenciales.")