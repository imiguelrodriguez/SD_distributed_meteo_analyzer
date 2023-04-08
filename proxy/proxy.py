import time
from concurrent import futures
from queue import Queue
import pickle
import grpc
import redis

from terminal import terminal_pb2, terminal_pb2_grpc


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

class ConnectionTerminalServiceServicer(terminal_pb2_grpc.ConnectionTServiceServicer):
    def SubscribeToProxy(self, connection, context):
        port = connection.port
        p.addTerminal(port)
        response = terminal_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class ResultsServiceServicer(terminal_pb2_grpc.ResultsServiceServicer):
    def SendResults(self, request, context):
        response = terminal_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class Proxy:
    MAX_SECONDS = 4

    def __init__(self):
        self._r = redis.Redis(host="localhost", port=6379)
        self._terminals = dict()  # this dictionary will store ports as keys and their correspondent stubs as values
        self._terminalsQueue = Queue()
        self._server = None
        self._serverPort = 50053
        while True:
            print(pickle.loads(self._r.rpop("wellness")))
            print(pickle.loads(self._r.rpop("pollution")))
            time.sleep(1)
        #self.serve()

    def tumblingWindow(self):
        pass

    def addTerminal(self, port):
        channel = grpc.insecure_channel('localhost:' + str(port))
        self._terminals[port] = terminal_pb2_grpc.ResultsServiceStub(channel)
        self._terminalsQueue.put(port)

        print("Added connection to terminal in port " + str(port))

    def serve(self):

        # listen on port 50053
        print('Starting Proxy server. Listening on port 50053 for terminals to establish connection.')
        with futures.ThreadPoolExecutor(max_workers=10) as pool:
            self._server = grpc.server(pool)
            terminal_pb2_grpc.add_ResultsServiceServicer_to_server(
                ResultsServiceServicer(), self._server)
            terminal_pb2_grpc.add_ConnectionTServiceServicer_to_server(
                ConnectionTerminalServiceServicer(), self._server)

            self._server.add_insecure_port('[::]:' + str(self._serverPort))
            self._server.start()
            try:
                self._server.wait_for_termination()
            except KeyboardInterrupt or Exception:
                print("Server stopped.")


p = Proxy()
