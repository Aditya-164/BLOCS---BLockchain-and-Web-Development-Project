from flask import Flask, request, jsonify, send_file
from Crypto.PublicKey import RSA
import os
import threading
import hashlib
from file_layer import Distribute, Assimilate
from network_layer import Network, Message
from typing import Optional, Dict, Any, List
import socket

# Constants and Global Variables
GENESIS_PORT = 5050
app = Flask(__name__)

# Initialize Flask application
cli_instance = None
private_key = None

class P2PFileStorage:
    def __init__(self, ip: str = "localhost", port: int = 5050, genesis_ip: Optional[str] = None) -> None:
        self.network = Network(ip)
        self.port = port
        self.genesis_ip = genesis_ip
        self.file_table: Dict[str, Dict[str, Any]] = {}
        self.network.start(port)
        self.msg_gen = Message(sender_ip=ip, sender_port=port)
        if genesis_ip:
            self.network.join_network()

    def _generate_file_id(self, file_content: bytes) -> str:
        file_hash = hashlib.sha256(file_content).hexdigest()
        return file_hash

    def distribute_file(self, file_path: str, private_key: bytes) -> Optional[str]:
        filename = os.path.basename(file_path)
        extension = os.path.splitext(filename)[1]
        file_size = os.path.getsize(file_path)
        peers = self.network.get_connections()
        num_shards = len(peers)
        if num_shards < 1:
            return None

        with open(file_path, 'rb') as file_obj:
            file_content = file_obj.read()
            file_id = self._generate_file_id(file_content)
            encrypted_shards, shard_mapping = Distribute(
                file_obj, private_key, num_shards=num_shards)

        peer_mapping = {peer_indx: -1 for peer_indx in range(len(peers))}
        for shard_index, shard in enumerate(encrypted_shards):
            peer = peers[shard_index % len(peers)]
            self._send_shard(peer, shard, shard_index, file_id)
            peer_mapping[shard_index % len(peers)] = shard_index

        self.file_table[file_id] = {
            "filename": filename,
            "size": file_size,
            "extension": extension,
            "shard_mapping": shard_mapping,
            "peer_mapping": peer_mapping,
        }
        return file_id

    def retrieve_file(self, file_id: str, private_key: bytes) -> Optional[str]:
        file_info = self.file_table.get(file_id)
        if not file_info:
            return None

        filename = file_info["filename"]
        shard_mapping = file_info["shard_mapping"]
        peer_mapping = file_info["peer_mapping"]
        peers = self.network.get_connections()
        shards = []
        for peer_indx, shard_index in peer_mapping.items():
            shard = self._request_shard(peers[peer_indx], file_id, shard_index)
            if shard:
                shards.append(shard)

        original_data = Assimilate(
            shards, shard_mapping, private_key)
        output_path = f"retrieved_{filename}"
        with open(output_path, 'wb') as out_file:
            out_file.write(original_data)
        return output_path

    def list_files(self) -> Dict[str, Dict[str, Any]]:
        return self.file_table

    def _send_shard(self, peer: str, shard: bytes, shard_index: int, file_id: str) -> None:
        message = {
            "file_id": file_id,
            "shard_index": shard_index,
            "shard_data": shard.hex()
        }
        self.network.send(peer, self.msg_gen.msg(
            message, "#STORE_SHARD"), hasResponse=1)

    def _request_shard(self, peer: socket.socket, file_id: str, shard_index: int) -> Optional[bytes]:
        message = {
            "file_id": file_id,
            "shard_index": shard_index
        }
        response = self.network.send(peer, self.msg_gen.msg(
            message, "#REQUEST_SHARD"), hasResponse=1)
        if response:
            shard_data = json.loads(response).get("message", {}).get("shard_data")
            return bytes.fromhex(shard_data) if shard_data else None
        return None

    def list_peers(self) -> List[tuple[str, int]]:
        return self.network.get_peers()

# Initialize the Genesis or regular node
def initialize_node(is_genesis, port, genesis_ip):
    global cli_instance
    cli_instance = P2PFileStorage(port=port, genesis_ip=genesis_ip)
    threading.Thread(target=cli_instance.network.listen_for_messages, daemon=True).start()

@app.route('/init', methods=['POST'])
def initialize():
    data = request.json
    is_genesis = data.get("is_genesis", False)
    port = data.get("port", GENESIS_PORT)
    genesis_ip = data.get("genesis_ip", None if is_genesis else data.get("genesis_ip"))
    initialize_node(is_genesis, port, genesis_ip)
    return jsonify({"message": "Node initialized successfully"}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    private_key_str = request.form.get("private_key")
    private_key = RSA.import_key(private_key_str)
    file_id = cli_instance.distribute_file(file_path=file.filename, private_key=private_key)
    return jsonify({"file_id": file_id}), 200 if file_id else 500

@app.route('/download/<file_id>', methods=['GET'])
def download_file(file_id):
    private_key_str = request.args.get("private_key")
    private_key = RSA.import_key(private_key_str)
    file_path = cli_instance.retrieve_file(file_id=file_id, private_key=private_key)
    return send_file(file_path, as_attachment=True) if file_path else ("File not found", 404)

@app.route('/list', methods=['GET'])
def list_files():
    files = cli_instance.list_files()
    return jsonify(files), 200

@app.route('/peers', methods=['GET'])
def list_peers():
    peers = cli_instance.list_peers()
    return jsonify(peers), 200

# Start the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
