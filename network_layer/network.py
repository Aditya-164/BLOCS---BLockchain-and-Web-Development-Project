import socket
import threading
import json
import logging
import os
from typing import List, Dict, Optional, Union, Tuple
# from .utils import bcolors
from .utils import print_colored
import network_layer.node as node
import network_layer.commands as commands
from .message import Message
from .config import BUFFER_SIZE

# Configure logging
logging.basicConfig(
    filename=os.path.join(os.curdir, "network.log"),
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Network(node.Node):
    HEADER_LEN: int = 10
    FORMAT: str = "utf-8"
    DISCONNECT_MSG: str = "!DISCONNECT"
    CONN_PORT: Optional[int] = None
    CONN_ADDR: Optional[tuple] = None

    def __init__(self, ip: str = "", port: Optional[int] = None, genesis_ip: Optional[str] = None, genesis_port: Optional[int] = None):
        self.SERVER_IP: str = ip

        if genesis_ip:
            self.GENESIS_NODE_ADDR: str = genesis_ip
        if genesis_port:
            self.GENESIS_NODE_PORT: int = genesis_port

        self.nodes_in_network: List[Dict[str, Union[str, int]]] = []
        self.nodes_in_network.append(
            {"ip_addr": self.GENESIS_NODE_ADDR, "port": self.GENESIS_NODE_PORT})

    def bindAndListen(self, port: int) -> None:
        self.SERVER_PORT: int = port
        self.SERVER_ADDR: tuple = (self.SERVER_IP, self.SERVER_PORT)

        self.server: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind(self.SERVER_ADDR)

        logging.info("[LISTENING...]")

        self.server.listen()

        while True:
            (conn, addr) = self.server.accept()
            # logging.debug(f"{conn} {addr}")

            thread = threading.Thread(target=self.handle, args=(conn, addr))
            thread.start()

           # logging.debug(f"{conn} connected")

    def start(self, port: int) -> None:

        node.SERVER_PORT = port

        thread = threading.Thread(target=self.bindAndListen, args=(port,))
        thread.start()
        return

    def handle(self, conn: socket.socket, addr: tuple) -> None:

        client_ip: Optional[str] = None
        client_port: Optional[int] = None

        print_colored(f"{addr} connected to server", "green", 5)

        connected: bool = True

        connectionError: bool = True
        ind: int = 0

        flag: int = 1

        msg_buffer: str = ''
        flag = 1
        while connected:

            full_msg: str = ''

            new_msg: bool = True

            while True:
                if new_msg:
                    if flag == 1:
                        msg = msg_buffer + conn.recv(2048).decode(self.FORMAT)
                    else:
                        msg = msg_buffer

                    # Controlling if msg is bigger than header
                    if len(msg) >= self.HEADER_LEN:
                        msg_len = int(msg[:self.HEADER_LEN])
                    else:
                        msg_buffer = msg
                        flag = 1
                        continue

                    full_msg += msg
                    if len(full_msg) - self.HEADER_LEN == msg_len:
                        msg_buffer = full_msg[self.HEADER_LEN + msg_len:]
                        new_msg = False

                        break
                    elif len(full_msg) - self.HEADER_LEN > msg_len:
                        msg_buffer = full_msg[self.HEADER_LEN + msg_len:]
                        full_msg = full_msg[:self.HEADER_LEN + msg_len]
                        new_msg = False
                        flag = 0
                        break
                    else:
                        msg_buffer = full_msg
                        flag = 1
                        full_msg = ''

                        continue

            if msg_len:
                ind += 1

                full_msg = full_msg[self.HEADER_LEN:]

                try:
                    msg = json.loads(full_msg)
                except:
                    print_colored(msg, "green")
                # msg=json.loads(msg)

                try:
                    index = self.message_logs.index(msg["id"])

                except:
                    index = -1
                    self.message_logs.append(msg["id"])

                if index != -1:
                    continue

                if len(self.message_logs) >= 50000:
                    logging.info(f"---{len(self.message_logs)}")
                    self.message_logs.pop(0)

                # CONNECT TO ME COMMAND
                if commands.NODE_CON_ADDR in msg['title']:

                    print_colored(f" {conn.getsockname()}", "blue")

                    message = msg["message"]

                    conn_addr = msg["message"].split(",")  # split ip and port

                    conn_ip = conn_addr[0]
                    conn_port = conn_addr[1]

                    client_ip = conn_ip
                    client_port = conn_port

                    if client_ip == "" or len(client_ip) == 0:

                        peername = conn.getpeername()
                        client_ip = peername[0]

                    conn_ip = client_ip

                    addr = (client_ip, int(conn_port))

                    print_colored(
                        f"{addr} wants to establish connection", "yellow")

                    try:
                        conn_index = self.connections.index(addr)
                    except:
                        conn_index = -1

                    if conn_index == -1:
                        # if connection has not established so far, connect to the node
                        self.connectToNode(conn_ip, int(conn_port))
                        print_colored(
                            f"{addr} Connection Established", "green")

                    else:
                        print_colored(
                            f"{addr} 2 Way Connection Established...", "green")

                if commands.CMD_JOIN_MSG in msg:

                    mssg = json.dumps(self.getSelfOrAdjacent())
                    mssg = f"{commands.MULTI_CONN_ADDR}{mssg}"
                    logging.debug(mssg)
                    conn.send(f"{mssg}".encode(self.FORMAT))
                    # (self.connections)
                    pass

                if commands.ASK_RANDOM_NODE in msg["title"]:
                    print_colored(f"{addr} ASKED RANDOM NODE ", "yellow")

                    conn_addr = msg["message"].split(",")  # split ip and port

                    conn_ip = conn_addr[0]
                    conn_port = conn_addr[1]

                    rndNode = json.dumps(self.getRandomNode())

                    conn.send(f"{rndNode}".encode(self.FORMAT))

                if commands.ASK_NODES_TO_CONNECT in msg["title"]:
                    print_colored(
                        f"{addr} ASKED NODES TO CONNECT", "yellow", 2)

                    got_nodes = self.getSelfOrAdjacent()
                    message = self.short_json_msg("", got_nodes)
                    self.reply(conn, message)
                    logging.debug("----------------------------------")
                    logging.debug(message)
                    # conn.send(f"{got_nodes}".encode(self.FORMAT))

                if "#GIVE_NODES_IN_NETWORK" in msg["title"]:

                    node_msg = self.short_json_msg("", self.nodes_in_network)

                    logging.debug(node_msg)

                    self.reply(conn, node_msg)

                if self.DISCONNECT_MSG in msg["title"]:
                    connected = False

                    print_colored(
                        f"{client_ip}:{client_port} DISCONNECTED", "red", 2)

                    self.remove_connection(conn, addr[0], addr[1])
                    break

                if "#BROADCAST" == msg["title"]:

                    self.broadcast(msg, True)

                    logging.debug(f"{msg}")

                    if msg['message'] == "#JOINED_IN_NETWORK":

                        msg_sender_ip = msg['sender_ip']
                        msg_sender_port = msg['sender_port']
                        if msg_sender_ip == "" or msg_sender_ip == None or len(msg_sender_ip) == 0:
                            msg_sender_ip = conn.getpeername()
                            msg_sender_ip = msg_sender_ip[0]

                        logging.debug(conn.getpeername())

                        print_colored(f"{msg['sender_ip']}:{msg['sender_port']} has joined to network", "green")

                        self.nodes_in_network.append(
                            {"ip_addr": msg_sender_ip, "port": msg['sender_port']})
                        logging.debug("NODES IN NETWORK ")
                        logging.debug(self.nodes_in_network)
                else:

                    logging.debug(msg["message"])
                
                if msg:
                    self.handle_messages(msg, conn)

        conn.close()

        return

    def handle_messages(self, msg: dict, conn: socket.socket) -> None:
        # can be overriden by the user to register custom message handlers
        return

    def reply(self, conn: socket.socket, msg_json: dict) -> None:
        message = json.dumps(msg_json)
        message = message.encode(self.FORMAT)
        conn.send(message)

    def join_network(self, ip: Optional[str] = None, port: Optional[int] = None) -> None:

        if ip is None:
            ip = self.GENESIS_NODE_ADDR
        if port is None:
            port = self.GENESIS_NODE_PORT

        logging.info(f"{ip}:{port}")
        conn = self.create_connection(ip, port)

        """
            Genesis node will return a ip address of a node
            new node will connect to this node
            new node will connect discover adjacent node
            #MULTI_CONN_ADDR
        """

        random_node = self.ask_random_node(
            conn, self.GENESIS_NODE_ADDR, self.GENESIS_NODE_PORT)

        node = json.loads(random_node)

        logging.debug(f"------->{node}")
        if node is None:

            self.remove_connection(conn, ip, port)

            logging.info("Network is not exist...")
            logging.info("Connecting to Genesis Node\n\n")

            self.connectToNode(self.GENESIS_NODE_ADDR, self.GENESIS_NODE_PORT)
            logging.debug("asadasd")

        else:
            """
                Ask adjacent from random node that given by network
            """
            self.remove_connection(conn, ip, port)
            # self.connectToNode(self.GENESIS_NODE_ADDR, self.GENESIS_NODE_PORT)
            logging.debug(node["ip_addr"])
            response = self.askNodes(node["ip_addr"], node["port"])

        temp_node = self.nodes[0]

        logging.debug(self.nodes[0])

        msg = Message().short_msg("#GIVE_NODES_IN_NETWORK", "")

        broadcast_msg = Message(self.SERVER_IP, self.SERVER_PORT).msg(
            "#JOINED_IN_NETWORK", "#BROADCAST")

        self.broadcast(broadcast_msg, isJson=True)

        nodes = self.send(temp_node, msg, 1)

        nodes = json.loads(nodes)

        nodes = nodes["message"]

        for node in nodes:

            try:
                index = self.nodes_in_network.index(node)
            except:
                index = -1

            if index == -1:

                self.nodes_in_network.append(node)
        
        return

    def ask_random_node(self, conn: socket.socket, address: str, port: int) -> str:

        # test_askRandMsg = Message().short_msg(commands.ASK_RANDOM_NODE, f"{self.SERVER_IP},{self.SERVER_PORT}")

        ask_random_message = self.short_json_msg(commands.ASK_RANDOM_NODE, f"{self.SERVER_IP},{self.SERVER_PORT}")

        message = ask_random_message

        msg = self.send(conn, message, 1)
        logging.debug(f"RESPONSE_RAND_NODE:{msg}")

        disconnect_msg = self.short_json_msg(self.DISCONNECT_MSG)
        self.send(conn, disconnect_msg)

        return msg

    def short_json_msg(self, title: str, message: str = "") -> dict:

        message = Message().short_msg(title, message)
        return message

    def askNodes(self, ip: str, port: int) -> None:

        conn = self.create_connection(ip, port)

        msg_json = self.short_json_msg(commands.ASK_NODES_TO_CONNECT)

        msg = self.send(conn, msg_json, 1)

        disconnect_msg = self.short_json_msg(self.DISCONNECT_MSG)

        self.send(conn, disconnect_msg)

        msg = json.loads(msg)
        nodes = msg["message"]
        logging.debug(type(nodes))

        print_colored(f"{len(nodes)} Node address recieved...", "cyan")
        logging.debug(nodes)

        for node in nodes:
            self.connectToNode(node["ip_addr"], node["port"])

    def create_connection(self, ip: str, port: int) -> socket.socket:

        CONN_ADDR = (ip, port)
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(CONN_ADDR)
        return connection

    def send(self, conn: socket.socket, msg_json: dict, hasResponse: int = 0) -> str:

        message = json.dumps(msg_json)
        temp_len = len(message)

        message = f'{temp_len:^{self.HEADER_LEN}}'+message
        message = message.encode(self.FORMAT)
        conn.send(message)
        if hasResponse:
            msg = conn.recv(BUFFER_SIZE).decode(self.FORMAT)
        else:
            msg = ""
        return msg

    def connectToNode(self, address: str, port: int) -> None:
        logging.debug(f"_______{address}_{port}_______________________-")
        self.CONN_ADDR = (address, port)

        if self.CONN_ADDR not in self.connections:

            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect(self.CONN_ADDR)

            x = {"ip_addr": address, "port": port}

            self.nodes.append(connection)
            self.connections.append(self.CONN_ADDR)
            self.connections_json.append(x)

            # msg=f"#NODE_CONN_ADDR({self.SERVER_IP},{self.SERVER_PORT})"

            msg = self.short_json_msg(commands.NODE_CON_ADDR, f"{self.SERVER_IP},{self.SERVER_PORT}")

            self.send(connection, msg)

        print_colored(f"Connected To->{address}:{port}", "green", 2)
        return

    def broadcast(self, data: Union[str, dict], isJson: bool = False) -> None:
        if not isJson:
            msg = self.short_json_msg("#BROADCAST", data)
        else:
            msg = data

        try:
            index = self.message_logs.index(msg["id"])

        except:
            index = -1
            self.message_logs.append(msg["id"])

        for node in self.nodes:

            try:
                self.send(node, msg)

            except:
                print_colored(
                    "MESSAGE COULDN'T SEND, RECIEVER MAY BE DISCONNECTED ", "red")

    def get_con(self, ip: str, port: int) -> socket.socket | None:
        indx = self.find_connection_index(ip, port)
        if indx == -1:
            return None
        return self.nodes[indx]

    def get_peers(self) -> List[Tuple[str, int]]:
        return self.connections

    def get_connections(self) -> List[socket.socket]:
        return self.nodes

    def stop(self) -> None:
        for node in self.nodes:
            node.close()
        self.server.close()
        return