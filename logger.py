import logging
import os

# la carpeta logs se crea al lado de este archivo
carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(carpeta, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(carpeta, "sistema.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

logger = logging.getLogger("software_fj")
