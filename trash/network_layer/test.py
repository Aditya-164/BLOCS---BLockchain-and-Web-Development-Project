# genesis_node.py

from network import Network

def setup_genesis_node():
    genesis = Network(ip="localhost", port=5050)
    genesis.start(5050)
    return genesis

if __name__ == "__main__":
    genesis_node = setup_genesis_node()
