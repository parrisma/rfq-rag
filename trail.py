import logging
import uuid
import os
from datetime import datetime

__lgr: logging.Logger = None

log_filename = f"./logs/log_{uuid.uuid4()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
log_filepath = os.path.join(os.getcwd(), log_filename)

__lgr = logging.getLogger('Rfq-Rag-Demo')
__lgr.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(log_filepath)
file_handler.setLevel(logging.DEBUG)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

        # Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
__lgr.addHandler(file_handler)
__lgr.addHandler(console_handler)


def log() -> logging.Logger:
    return __lgr
