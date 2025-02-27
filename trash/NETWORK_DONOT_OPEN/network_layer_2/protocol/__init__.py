import asyncio
from kademlia.network import Server

async def start_bootstrap_node(port):
    server = Server()
    await server.listen(port)
    print(f"Bootstrap node started on port {port}")
    return server


async def main():
    bootstrap_servers = await asyncio.gather(
        start_bootstrap_node(8468),
        start_bootstrap_node(8469),
        start_bootstrap_node(8470)
    )

    try:
        # Keep running until interrupted
        await asyncio.Event().wait()
    finally:
        # Stop all servers on exit
        for server in bootstrap_servers:
            await server.stop()
            print("Bootstrap node stopped")


if __name__ == "__main__":
    asyncio.run(main())
