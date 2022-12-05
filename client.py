import zmq
import logging
import time
import json


class Node:
    def __init__(self, peerlist, port="5556", id="node"):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("node")
        self.logger.setLevel(logging.INFO)

        self.context = zmq.Context()

        self.publisher = self.context.socket(zmq.PUB)
        self.publisher.bind(f"tcp://*:{port}")

        self.logger.info("Node spawned, finding peers...")

        self.listener = self.context.socket(zmq.SUB)

        for peer in peerlist:
            self.logger.info(f"Attempting to connect to {peer}...")
            self.listener.connect(peer)
            self.logger.info(f"Connected to {peer}")

        while True:
            self.loop()

    def loop(self):
        raw_data = self.listener.recv_string()
        message = json.load(raw_data)
        self.logger.info(message)


def main():
    ports = [5555, 5556, 5557, 5558, 5559, 5560]
    nodes = []
    for i, port in enumerate(ports):
        # make sure we don't pass the nodes' own adress in the peer list
        peer_ports = ports[0:i] + ports[i+1:]
        peerlist = [f"tcp://localhost:{p}" for p in peer_ports]
        nodes.append(Node(peerlist, port))
    while True:
        pass


if __name__ == "__main__":
    main()
