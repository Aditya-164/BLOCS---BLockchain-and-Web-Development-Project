from network import Network

node = Network(ip="localhost", port=5052)
node.start(port=5052)

node.connect_to_node("localhost", 5050)
print("NODE ON")


_ = input("Press any key to continue")

    