import socket
import time

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
        try:
            connectionT = userTerminal_pb2.ConnectionT()
            connectionT.port = self._port
            print("Chosen port for terminal: " + str(self._port))
            stub = userTerminal_pb2_grpc.ConnectionTServiceStub(self._subscribeChannel)
            stub.SubscribeToProxy(connectionT)
        except Exception as e:
            print("There is a problem establishing connection with the proxy server.")
            print(e)

    def plot(self):
        while True:
            print("I'm plotting")
            time.sleep(3)
        pass


if __name__ == '__main__':
    t = Terminal()

