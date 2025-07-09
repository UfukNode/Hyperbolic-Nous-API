import logging
import sys
from datetime import datetime

def setup_logger(name: str = "hyperbolic_api"):
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(message)s"
    )
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger
