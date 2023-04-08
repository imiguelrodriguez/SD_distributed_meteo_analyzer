import socket

import grpc

import terminal_pb2

import terminal_pb2_grpc


class Terminal:
    def __init__(self):
        self._subscribeChannel = None
        sock = socket.socket()
        sock.bind(('', 0))
        self._port = sock.getsockname()[1]
        self.subscribeToP()

    def subscribeToP(self):
        # subscribe channel to send the chosen port to the LB
        self._subscribeChannel = grpc.insecure_channel('localhost:50053')
        connectionT = terminal_pb2.ConnectionT()
        connectionT.port = self._port
        print("Chosen port for terminal: " + str(self._port))
        stub = terminal_pb2_grpc.ConnectionTServiceStub(self._subscribeChannel)
        stub.SubscribeToProxy(connectionT)

    def plot(self):
        pass


t = Terminal()

