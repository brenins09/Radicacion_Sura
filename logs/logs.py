import logging
import os
from datetime import datetime

# -------- LOG PRINCIPAL --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(BASE_DIR, "logs")
os.makedirs(logs_dir, exist_ok=True)

log_filename = os.path.join(logs_dir, f"ejecucion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logger = logging.getLogger("ejecucion_logger")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(log_filename)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# -------- LOG DE ERRORES SEPARADO --------
errores_dir = os.path.join(BASE_DIR, "logs_errores")
os.makedirs(errores_dir, exist_ok=True)

errores_filename = os.path.join(errores_dir, f"errores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

error_logger = logging.getLogger("errores_logger")
error_logger.setLevel(logging.ERROR)

error_handler = logging.FileHandler(errores_filename)
error_handler.setLevel(logging.ERROR)

error_handler.setFormatter(formatter)
error_logger.addHandler(error_handler)

# -------- USO --------
#slogger.info("Este es un log general.")
#serror_logger.error("Este es un error crítico.")
