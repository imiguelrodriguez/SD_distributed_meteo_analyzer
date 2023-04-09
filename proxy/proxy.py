import pickle
import time
from concurrent import futures
from queue import Queue

import grpc
import redis

import proxy_pb2
import proxy_pb2_grpc
from terminal import userTerminal_pb2_grpc, userTerminal_pb2


class WellnessAux:
    def __init__(self, wellness, datetime):
        self.wellness = wellness
        self.timestamp = datetime

    def __str__(self):
        return "Wellness: " + str(self.wellness) + " Timestamp: " + str(self.timestamp)


class PollutionAux:
    def __init__(self, pollution, datetime):
        self.pollution = pollution
        self.timestamp = datetime

    def __str__(self):
        return "Pollution: " + str(self.pollution) + " Timestamp: " + str(self.timestamp)


class ConnectionTServiceServicer(userTerminal_pb2_grpc.ConnectionTServiceServicer):
    def SubscribeToProxy(self, connectionT, context):
        port = connectionT.port
        p.addTerminal(port)
        response = userTerminal_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class ResultsServiceServicer(proxy_pb2_grpc.ResultsServiceServicer):
    def SendResults(self, request, context):
        response = proxy_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class Proxy:
    MAX_SECONDS = 4

    def __init__(self):
        try:
            self._r = redis.Redis(host="localhost", port=6379)
        except Exception as e:
            print("There is a problem when connecting to the REDIS server.")
            print(e)
        self._terminals = dict()  # this dictionary will store ports as keys and their correspondent stubs as values
        self._terminalsQueue = Queue()
        self._server = None
        self._serverPort = 50055

    def tumblingWindow(self):
        while True:
            print(pickle.loads(self._r.rpop("wellness")))
            print(pickle.loads(self._r.rpop("pollution")))
            time.sleep(1)

    def addTerminal(self, port):
        channel = grpc.insecure_channel('localhost:' + str(port))
        self._terminals[port] = proxy_pb2_grpc.ResultsServiceStub(channel)
        self._terminalsQueue.put(port)

        print("Added connection to terminal in port " + str(port))

    def serve(self):

        # listen on port 50055
        print('Starting Proxy server. Listening on port 50055 for terminals to establish connection.')
        with futures.ThreadPoolExecutor(max_workers=10) as pool:
            self._server = grpc.server(pool)
            proxy_pb2_grpc.add_ResultsServiceServicer_to_server(
                ResultsServiceServicer(), self._server)
            userTerminal_pb2_grpc.add_ConnectionTServiceServicer_to_server(
                ConnectionTServiceServicer(), self._server)

            self._server.add_insecure_port('[::]:' + str(self._serverPort))
            self._server.start()
            try:
                self._server.wait_for_termination()
            except KeyboardInterrupt or Exception:
                print("Server stopped.")


if __name__ == '__main__':
    p = Proxy()

    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(p.serve)
        executor.submit(p.tumblingWindow)
