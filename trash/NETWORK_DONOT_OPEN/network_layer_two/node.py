# network_layer/node.py

import socket
import threading
import pickle
from network_layer.handlers import DataPacket, DataHandler
from network_layer.utils import connect_socket
from network_layer.config import BUFFER_SIZE, MAX_CONNECTIONS, TIMEOUT

class Node:
    def __init__(self, node_id, host, port):
        self.node_id = node_id
        self.host = host
        self.port = port
        self.peers = set()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen(MAX_CONNECTIONS)

    def start_node(self):
        threading.Thread(target=self.listen_for_peers).start()
        print(f"Node {self.node_id} started on {self.host}:{self.port}")

    def connect_to_bootstrap(self):
        try:
            s = connect_socket(*self.bootstrap_address)
            s.sendall(pickle.dumps(self.node_id))
            peer_list = pickle.loads(s.recv(BUFFER_SIZE))
            self.peers.update(peer_list)
            print(f"Node {self.node_id} connected to bootstrap; Peers: {self.peers}")
        except Exception as e:
            print(f"Connection to bootstrap failed: {e}")

    def listen_for_peers(self):
        while True:
            conn, _ = self.socket.accept()
            threading.Thread(target=self.handle_peer, args=(conn,)).start()

    def handle_peer(self, conn):
        try:
            data = conn.recv(BUFFER_SIZE)
            packet = pickle.loads(data)
            self.handle_data(packet)
        finally:
            conn.close()

    def send_data(self, peer, data):
        try:
            s = connect_socket(peer[0], peer[1])
            packet = DataPacket(self.node_id, data)
            s.sendall(pickle.dumps(packet))
        except Exception as e:
            print(f"Failed to send data to {peer}: {e}")

    def broadcast_data(self, data):
        for peer in self.peers:
            self.send_data(peer, data)

    def handle_data(self, packet):
        DataHandler.handle_data(self, packet)
