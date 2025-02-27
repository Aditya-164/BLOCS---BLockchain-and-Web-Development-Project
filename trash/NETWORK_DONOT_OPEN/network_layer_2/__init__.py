import asyncio
from protocol.kad import KademliaNode
from protocol.gossipsub import GossipProtocol
from utils import setup_logging

logger = setup_logging()

async def main():
    port = 8969
    node = KademliaNode(port)
    gossip = GossipProtocol(node)
    await node.start()
    logger.info(f"Kademlia node started on port {port}")
    gossip_task = asyncio.create_task(gossip.start_gossip())

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        pass
    finally:
        gossip_task.cancel()
        await node.stop()
        logger.info("Kademlia node shut down.")

if __name__ == "__main__":
    asyncio.run(main())
