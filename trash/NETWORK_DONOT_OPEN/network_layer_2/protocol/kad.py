import asyncio
import kademlia
from kademlia.network import Server
from .confignetwork  import BOOTSTRAP_NODES

class KademliaNode:
    def __init__(self, port):
        self.server = Server()
        self.port = port

    async def start(self):
        await self.server.listen(self.port)
        print("Server is listening.")
        try:
            await self.server.bootstrap(BOOTSTRAP_NODES)
            print("Bootstrap process started")
        except Exception as e:
            print(f"Error during bootstrap: {e}")
        print(f"Bootstrappable neighbors: {self.server.bootstrappable_neighbors()}")
    async def stop(self):
        await self.server.stop()

    async def store_data(self, key, value):
        await self.server.set(key, value)

    async def retrieve_data(self, key):
        return await self.server.get(key)