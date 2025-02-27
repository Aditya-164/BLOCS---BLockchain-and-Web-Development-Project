from abc import ABC, abstractmethod
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class DataHandler(ABC):
    """Abstract base class for data handlers"""

    @abstractmethod
    async def handle_data(self, data: Dict[str, Any], sender_id: str) -> None:
        """Handle incoming data from peers"""
        pass


class DefaultDataHandler(DataHandler):
    """Default implementation of data handler"""

    async def handle_data(self, data: Dict[str, Any], sender_id: str) -> None:
        logger.info(f"Received data from {sender_id}: {data}")
