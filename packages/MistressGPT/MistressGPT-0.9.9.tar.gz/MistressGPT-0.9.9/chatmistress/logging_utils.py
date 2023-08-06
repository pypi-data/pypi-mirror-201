import os
import sys
from dotenv import load_dotenv
from loguru import logger
from pathlib import Path

load_dotenv()
logging_dir = Path(os.getenv("LOGGING_DIR", "logs"))
logging_dir.mkdir(exist_ok=True)

logger.remove(0)
logger.add(logging_dir / "mistressgpt.log", rotation="10 MB",
           level=os.getenv("LOG_LEVEL", "ERROR"))
logger.add(sys.stderr, level=os.getenv("LOG_LEVEL", "ERROR"))
