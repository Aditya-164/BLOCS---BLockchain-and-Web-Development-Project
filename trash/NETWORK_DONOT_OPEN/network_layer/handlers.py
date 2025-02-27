from typing import Any
# network_layer/handlers.py

class DataPacket:
    def __init__(self, sender_id: int, data: Any) -> None:
        self.sender_id: int = sender_id
        self.data: Any = data

    def __str__(self) -> str:
        return f"{self.sender_id}: {self.data}"

class DataHandler:
    @staticmethod
    def handle_data(node, packet: DataPacket) -> None:
        print(f"Node {node.node_id} received data: {packet}")
