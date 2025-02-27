import pytest
import time
import json
import threading
from network_layer.network import Network


@pytest.fixture(scope="session")
def genesis_node():
    """Fixture to create and start a genesis node in a separate thread"""
    node = Network("localhost")
    thread = threading.Thread(target=node.start, args=(5050,))
    thread.start()
    time.sleep(1)  # Allow time for node to start
    yield node
    # Cleanup
    node.stop()
    thread.join()


@pytest.fixture(scope="session")
def peer_node():
    """Fixture to create and start a peer node in a separate thread"""
    node = Network("localhost")
    thread = threading.Thread(target=node.start, args=(5051,))
    thread.start()
    time.sleep(1)  # Allow time for node to start
    yield node
    # Cleanup
    node.stop()
    thread.join()


def test_genesis_node_creation(genesis_node):
    """Test if genesis node is created and listening"""
    assert genesis_node.SERVER_IP == "localhost"
    assert genesis_node.SERVER_PORT == 5050
    assert genesis_node.server is not None


def test_peer_node_creation(peer_node):
    """Test if peer node is created and listening"""
    assert peer_node.SERVER_IP == "localhost"
    assert peer_node.SERVER_PORT == 5051
    assert peer_node.server is not None


def test_node_connection(genesis_node, peer_node):
    """Test if peer node can connect to genesis node"""
    thread = threading.Thread(target=peer_node.join_network, args=(genesis_node.SERVER_IP, genesis_node.SERVER_PORT))
    thread.start()
    time.sleep(5)  # Allow time for connection

    # Check if genesis node is in peer's connections
    assert len(peer_node.connections) > 0
    assert (genesis_node.SERVER_IP, genesis_node.SERVER_PORT) in peer_node.connections


def test_message_broadcast(genesis_node, peer_node):
    """Test broadcasting messages between nodes"""
    thread = threading.Thread(target=peer_node.join_network, args=(genesis_node.SERVER_IP, genesis_node.SERVER_PORT))
    thread.start()
    time.sleep(4)  # Allow time for connection

    # Create a message to broadcast
    test_message = "Hello, network!"
    peer_node.broadcast(test_message)
    time.sleep(1)  # Allow time for message propagation

    # Check if message is in message logs
    assert len(peer_node.message_logs) > 0
    assert len(genesis_node.message_logs) > 0


def test_direct_message(genesis_node, peer_node):
    """Test sending direct messages between nodes"""
    peer_node.join_network()
    time.sleep(1)  # Allow time for connection

    # Create a direct message
    test_message = peer_node.short_json_msg("#DIRECT_MESSAGE", "Hello, genesis!")

    # Get connection to genesis node
    genesis_conn = peer_node.get_con(ip=genesis_node.SERVER_IP, port=genesis_node.SERVER_PORT)

    # Send message and get response
    response = peer_node.send(genesis_conn, test_message, hasResponse=1)

    # Verify response is received
    assert response != ""


def test_node_discovery(genesis_node, peer_node):
    """Test if new nodes can discover existing network nodes"""
    peer_node.join_network()
    time.sleep(1)  # Allow time for connection

    # Check if nodes_in_network list is populated
    assert len(peer_node.nodes_in_network) > 0
    assert {"ip_addr": genesis_node.SERVER_IP, "port": genesis_node.SERVER_PORT} in peer_node.nodes_in_network


def test_node_disconnect(genesis_node, peer_node):
    """Test proper handling of node disconnection"""
    peer_node.join_network()
    time.sleep(1)  # Allow time for connection

    # Send disconnect message
    disconnect_msg = peer_node.short_json_msg(peer_node.DISCONNECT_MSG)
    genesis_conn = peer_node.nodes[0]
    peer_node.send(genesis_conn, disconnect_msg)
    time.sleep(1)  # Allow time for disconnection

    # Check if connection is removed
    assert (genesis_node.SERVER_IP, genesis_node.SERVER_PORT) not in peer_node.connections


def test_message_format(genesis_node, peer_node):
    """Test if messages are properly formatted"""
    # Create a test message
    test_message = peer_node.short_json_msg("#TEST", "Test message")

    # Verify message structure
    assert "id" in test_message
    assert "title" in test_message
    assert "message" in test_message
    assert "time" in test_message

    # Verify message can be parsed as JSON
    assert json.loads(json.dumps(test_message))


def test_invalid_connection():
    """Test handling of connection to invalid address"""
    node = Network("localhost")
    with pytest.raises(Exception):
        # Try to connect to invalid port
        node.create_connection("localhost", 9999)
