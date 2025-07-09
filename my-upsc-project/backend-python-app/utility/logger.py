# In utility/logger.py

import logging
import sys

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"), # Log to a file
        logging.StreamHandler(sys.stdout) # Also log to the console
    ]
)

logger = logging.getLogger(__name__)