import logging

logging.basicConfig(
    filename="network.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)

logger = logging.getLogger("NetworkLayer")
