import socket
import random
import os
import logging
from typing import List, Tuple, Union, Optional
from network_layer.message import Message

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.curdir, "network.log"),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Node:
    SERVER_IP: str = socket.gethostbyname(socket.gethostname())
    SERVER_PORT: Optional[int] = None
    SERVER_ADDR: Optional[Tuple[str, int]] = None

    GENESIS_NODE_ADDR: str = "localhost"  # boot node address
    GENESIS_NODE_PORT: int = 5050  # boot node port

    nodes: List[socket.socket] = list()  # connections
    connections: List[Tuple[str, int]] = list()  # connection addresses
    incomingConnections: List[socket.socket] = list()
    connections_json: List[dict] = list()

    message_logs: List[str] = list()

    nodes_in_network: List[dict] = list()

    isJoinedNetwork: bool = False

    def __init__(self, ip: str = SERVER_IP, port: Optional[int] = SERVER_PORT) -> None:
        self.SERVER_IP = ip
        self.SERVER_PORT = port
        self.SERVER_ADDR = (ip, port)

    def totalConection(self) -> int:
        return len(self.connections)

    def find_addr_index(self, ip: str, port: int) -> int:
        index = 0
        result = -1
        for node in self.connections:
            if (node[0] == ip and node[1] == port):
                result = index
                break
            index += 1
        return result

    def find_connection_index(self, ip: str, port: int) -> int:
        index = 0
        result = -1
        for node in self.nodes:
            peername = node.getpeername()
            if (peername[0] == ip and peername[1] == port):
                result = index
                break
            index += 1
        return result

    def find_json_index(self, ip: str, port: int) -> int:
        index = 0
        result = -1
        for node in self.connections_json:
            if (node["ip_addr"] == ip and node["port"] == port):
                result = index
                break
            index += 1
        return result

    def getRandomNode(self) -> dict:
        json_temp = self.connections_json.copy()  # all active connections are copied
        total_node = self.totalConection()  # calculate total connected node
        if total_node == 0:
            # if there is no any connection, return self ip and port
            return {"ip_addr": self.SERVER_IP, "port": self.SERVER_PORT}
        rnd = random.randint(0, total_node-1)  # random index
        return json_temp[rnd]

    def remove_connection(self, conn: socket.socket, ip: str, port: int) -> None:
        try:
            conn_index = self.find_connection_index(ip, port)
        except:
            conn_index = -1
        if (conn_index != -1):
            self.nodes.pop(conn_index)
        try:
            node_index = self.find_addr_index(ip, port)
        except:
            node_index = -1
        if (node_index != -1):
            self.connections.pop(node_index)
        try:
            node_index = self.find_json_index(ip, port)
        except:
            node_index = -1
        if (node_index != -1):
            self.connections_json.pop(node_index)
        logging.debug(self.nodes)
        logging.debug(self.connections)

    def getSelfOrAdjacent(self) -> Union[str, List[dict]]:
        total_adj = self.totalConection()
        server_json = {"ip_addr": self.SERVER_IP, "port": self.SERVER_PORT}
        if total_adj == 0:
            return self.merge_command("NODE_CON_ADDR", f"({self.SERVER_IP},{self.SERVER_PORT})")
        if total_adj == 1:
            temp_json_list = self.connections_json.copy()
            temp_json_list.append(server_json)
            return temp_json_list
        if (total_adj >= 2):
            copy_json = self.connections_json.copy()
            copy_json.append(server_json)
            total_return = random.randint(
                2, total_adj+1)  # +1 is for self address
            arr = list(range(0, total_adj+1))
            random.shuffle(arr)
            arr = arr[0:total_return]
            logging.debug(f"{total_return} , {arr}")
            temp_json_list = list()
            for i in arr:
                temp_json_list.append(copy_json[i])
            logging.debug(temp_json_list)
            return temp_json_list

    @classmethod
    def set_node(cls, ip: str, port: int) -> None:
        cls.SERVER_PORT = port
        cls.SERVER_IP = ip
        cls.SERVER_ADDR = (ip, port)

    @staticmethod
    def calculateMsgLen(msg: str) -> bytes:
        message = msg.encode("utf-8")
        msg_len = len(message)
        send_len = str(msg_len).encode("utf-8")
        send_len += b' ' * (64 - len(send_len))
        return send_len

    @staticmethod
    def merge_command(cmd: str, msg: str) -> str:
        message = f"{cmd}({msg})"
        logging.debug(message)
        return message

    @staticmethod
    def split_command(cmd: str, msg: str) -> str:
        length = len(cmd)
        message = msg[length+1:-1]
        logging.debug(message)
        return message

    def create_message(self, msg: str, title: str, sender_ip: str = SERVER_IP, sender_port: Optional[int] = SERVER_PORT, reciever_ip: str = "all", reciever_port: Optional[int] = None) -> str:
        if sender_port is None:
            sender_port = self.SERVER_PORT
        message = Message(sender_ip, sender_port, reciever_ip, reciever_port)
        return message.msg(msg, title)
