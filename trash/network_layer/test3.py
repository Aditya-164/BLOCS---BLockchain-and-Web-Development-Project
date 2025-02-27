# client1.py

from network import Network

def setup_client_node(ip, port):
    client = Network(ip=ip, port=port)
    client.start(port)
    return client

if __name__ == "__main__":
    client1 = setup_client_node("localhost", 5051)
    client1.connect_to_node("localhost", 5050)  # Connect to Genesis
    client1.broadcast({"message": "Hello from Client 1"})
    client1.send_direct_message("192.168.56.3", 5052, {"message": "Direct message from Client 1"})
