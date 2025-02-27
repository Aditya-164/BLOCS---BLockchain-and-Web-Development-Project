import asyncio
import random
from .confignetwork import GOSSIP_INTERVAL

class GossipProtocol:
    def __init__(self, node):
        self.node = node

    async def start_gossip(self):
        while True:
            print(f"CHIGGA HIGH{self.node}")
            await self.perform_gossip()
            await asyncio.sleep(GOSSIP_INTERVAL)

    async def perform_gossip(self):
        peers = self.node.server.bootstrappable_neighbors()
        print(peers)
        if not peers:
            print("LONELY CHIGGA NO PEERS")
            return
        # selected_peers = random.sample(peers, min(len(peers), 5))
        for peer in peers:
            data_to_share = "HI CHIGGA"
            await self.gossip_to_peer(peer, data_to_share)

    async def gossip_to_peer(self, peer, data):
        try:
            await self.node.server.set(peer, data)
            print(f"Gossiped with peer {peer}")
        except Exception as e:
            print(f"Failed to gossip with peer {peer}: {e}")
