import logging
import os
import sys

logging_str = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
logging_dir = 'logs'
logging_filepath = os.path.join(logging_dir, 'network_security.log')
os.makedirs(logging_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(logging_filepath),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
#logger.info("Logging is set up for the Network Security module.")