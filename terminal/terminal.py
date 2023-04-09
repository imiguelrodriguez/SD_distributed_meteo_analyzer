import socket
import grpc

import userTerminal_pb2
import userTerminal_pb2_grpc


class Terminal:
    def __init__(self):
        self._subscribeChannel = None
        sock = socket.socket()
        sock.bind(('', 0))
        self._port = sock.getsockname()[1]
        self.subscribeToProxy()
        self.plot()

    def subscribeToProxy(self):
        # subscribe channel to send the chosen port to the LB
        self._subscribeChannel = grpc.insecure_channel('localhost:50055')
        connectionT = userTerminal_pb2.ConnectionT()
        connectionT.port = self._port
        print("Chosen port for terminal: " + str(self._port))
        stub = userTerminal_pb2_grpc.ConnectionTServiceStub(self._subscribeChannel)
        stub.SubscribeToProxy(connectionT)

    def plot(self):
        print("I'm plotting")
        pass


if __name__ == '__main__':
    t = Terminal()

