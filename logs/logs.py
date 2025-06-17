import logging
from datetime import datetime

# Desactiva los logs innecesarios (WebDriver Manager y otras librerías)
logging.getLogger('webdriver_manager').setLevel(logging.CRITICAL)
logging.getLogger('requests').setLevel(logging.CRITICAL)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

# Configura el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Ajusta el nivel a INFO o ERROR según lo que necesites

# Crea un manejador para guardar los logs en un archivo, con un nombre único por ejecución
log_filename = rf'C:\Users\bcalonso.RPA01\Documents\Historico_OCGN\Historico\logs\ejecucion_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'  # Nombre único por ejecución
file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)  # Solo guarda logs de nivel INFO o superior

# Define el formato para los logs
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)

# Agrega el manejador al logger
logger.addHandler(file_handler)
