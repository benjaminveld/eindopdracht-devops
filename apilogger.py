import logging
import sys

logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("api.log")

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)