#!/usr/bin/env python3
import logging, logging.handlers, os
from pythonjsonlogger import jsonlogger

os.makedirs("logs", exist_ok=True)
handler = logging.handlers.TimedRotatingFileHandler(
    filename="logs/inventory.log", when="midnight", backupCount=7
)
fmt = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s %(process)d %(threadName)s')
handler.setFormatter(fmt)
logger = logging.getLogger("inventory")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.info("startup", extra={"synthetic": True, "seed": 12345})
