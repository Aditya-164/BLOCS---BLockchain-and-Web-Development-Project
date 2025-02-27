import socket
import threading
import pickle
from typing import Set, Tuple, Optional, Any
from .handlers import DataPacket, DataHandler
from .utils import connect_socket
from .logger import logger
from .config import BUFFER_SIZE, MAX_CONNECTIONS, RETRY_COUNT

class Node:
    def __init__(self, node_id: str, host: str, port: int, 
                 bootstrap_address: Optional[Tuple[str, int]] = None) -> None:
        self.node_id: str = node_id
        self.host: str = host
        self.port: int = port
        self.bootstrap_address: Optional[Tuple[str, int]] = bootstrap_address
        self.peers: Set[Tuple[str, str, int]] = set()  # Each peer is stored as a tuple (node_id, host, port)
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(MAX_CONNECTIONS)
        self.running: bool = True

    def __str__(self) -> str:
        return f"Node {self.node_id} on {self.host}:{self.port}"

    def start_node(self) -> None:
        threading.Thread(target=self.listen_for_peers, daemon=True).start()
        if self.bootstrap_address:
            self.connect_to_bootstrap()
        logger.info(f"Node {self.node_id} started on {self.host}:{self.port}")

    def get_peers(self) -> Set[Tuple[str, str, int]]:
        return self.peers

    def connect_to_bootstrap(self) -> None:
        try:
            s: socket.socket = connect_socket(*self.bootstrap_address)
            s.sendall(pickle.dumps((self.node_id, self.host, self.port)))
            peer_list: Set[Tuple[str, str, int]] = pickle.loads(s.recv(BUFFER_SIZE))
            self.peers.update(peer_list)
            logger.info(f"Node {self.node_id} connected to bootstrap; Peers: {self.peers}")
            s.close()
            self.connect_to_peers()
        except Exception as e:
            logger.error(f"Node {self.node_id} failed to connect to bootstrap: {e}")
            self.shutdown()

    def connect_to_peers(self) -> None:
        for peer in self.peers:
            peer_id, peer_host, peer_port = peer
            if peer_id != self.node_id:
                for attempt in range(RETRY_COUNT):
                    try:
                        s: socket.socket = connect_socket(peer_host, peer_port)
                        s.sendall(pickle.dumps(DataPacket(self.node_id, f"Hello from Node {self.node_id}")))
                        logger.info(f"Node {self.node_id} connected to peer {peer_id} at {peer_host}:{peer_port}")
                        s.close()
                        break
                    except Exception as e:
                        logger.warning(f"Node {self.node_id} failed to connect to peer {peer_id} "
                                    f"at {peer_host}:{peer_port} on attempt {attempt + 1}: {e}")
                        if attempt == RETRY_COUNT - 1:
                            logger.error(f"Node {self.node_id} exhausted retries for peer {peer_id}")

    def listen_for_peers(self) -> None:
        while self.running:
            try:
                conn, _ = self.socket.accept()
                threading.Thread(target=self.handle_peer, args=(conn,), daemon=True).start()
            except Exception as e:
                logger.error(f"Node {self.node_id} encountered error while listening for peers: {e}")
                self.shutdown()

    def handle_peer(self, conn: socket.socket) -> None:
        try:
            data: bytes = conn.recv(BUFFER_SIZE)
            packet: DataPacket = pickle.loads(data)
            self.handle_data(packet)
        except Exception as e:
            logger.error(f"Node {self.node_id} failed to handle data from peer: {e}")
        finally:
            conn.close()

    def send_data(self, peer: Tuple[str, str, int], data: Any) -> None:
        try:
            peer_id, peer_host, peer_port = peer
            s: socket.socket = connect_socket(peer_host, peer_port)
            packet: DataPacket = DataPacket(self.node_id, data)
            s.sendall(pickle.dumps(packet))
            s.close()
            logger.info(f"Node {self.node_id} sent data to peer {peer_id} at {peer_host}:{peer_port}")
        except Exception as e:
            logger.error(f"Node {self.node_id} failed to send data to peer {peer_id} at {peer_host}:{peer_port}: {e}")

    def broadcast_data(self, data: Any) -> None:
        for peer in self.peers:
            self.send_data(peer, data)

    def handle_data(self, packet: DataPacket) -> None:
        DataHandler.handle_data(self, packet)

    def shutdown(self) -> None:
        self.running = False
        self.socket.close()
        logger.info(f"Node {self.node_id} on {self.host}:{self.port} has shut down.")
