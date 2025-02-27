# import random
import json
from .node import Node

class Network(Node):
    def __init__(self, ip, port, genesis_node_ip=None, genesis_node_port=None):
        super().__init__(ip, port)
        self.genesis_node_ip = genesis_node_ip
        self.genesis_node_port = genesis_node_port
        self.peers_in_network = [{"ip": ip, "port": port}]

    def join_network(self):
        if self.genesis_node_ip:
            conn = self.connect_to_peer(self.genesis_node_ip, self.genesis_node_port)
            self.send_message(conn, json.dumps({"type": "JOIN_REQUEST", "ip": self.ip, "port": self.port}))
            response = conn.recv(1024).decode()
            self.peers_in_network = json.loads(response)
            print(f"[NETWORK INFO] Joined network with peers: {self.peers_in_network}")
        
    def broadcast(self, message):
        for peer in self.peers_in_network:
            conn = self.connect_to_peer(peer["ip"], peer["port"])
            self.send_message(conn, json.dumps({"type": "BROADCAST", "message": message, "sender": (self.ip, self.port)}))
            conn.close()
