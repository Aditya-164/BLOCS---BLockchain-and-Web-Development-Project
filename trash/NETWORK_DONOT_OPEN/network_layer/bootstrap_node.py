import pickle
import threading
from typing import Set, Tuple
from .node import Node
from .logger import logger
from .config import BUFFER_SIZE

class BootstrapNode(Node):
    def __init__(self, node_id: str, host: str, port: int) -> None:
        super().__init__(node_id, host, port)
        self.peers: Set[Tuple[str, int]] = set()

    def start_bootstrap_node(self) -> None:
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        logger.info(f"Bootstrap node {self.node_id} started on {self.host}:{self.port}")

    def handle_peer(self, conn) -> None:
        try:
            data = conn.recv(BUFFER_SIZE)
            new_peer: Tuple[str, int] = pickle.loads(data)
            conn.sendall(pickle.dumps(list(self.peers)))
            self.peers.add(new_peer)
            logger.info(f"Bootstrap node {self.node_id} added new peer: {new_peer}")
            logger.info(f"Updated peers list: {self.peers}")
        except Exception as e:
            logger.error(f"Bootstrap node {self.node_id} failed to handle new peer: {e}")
        finally:
            conn.close()

    def shutdown(self) -> None:
        super().shutdown()
        logger.info(f"Bootstrap node {self.node_id} has shut down.")
