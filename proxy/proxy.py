import datetime
import os
import pickle
import socket
import sys
import time
from concurrent import futures
import grpc
import redis

import proxy_pb2
import proxy_pb2_grpc
import redisQueues
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


class Proxy:
    MAX_SECONDS = 4

    def __init__(self):
        try:
            self._r = redis.Redis(host="localhost", port=6379)
        except Exception as e:
            print("There is a problem when connecting to the REDIS server.")
            print(e)
            sys.exit(-1)
        self._terminals = dict()  # this dictionary will store ports as keys and their correspondent stubs as values
        self._server = None
        sock = socket.socket()
        sock.bind(('', 0))
        self._serverPort = sock.getsockname()[1]
        with open(".." + os.sep + "proxyPort.txt", "w") as f:
            f.write(str(self._serverPort))
            f.close()

    def tumblingWindow(self):
        while True:
            wellness = []
            pollution = []
            end_time = time.time() + self.MAX_SECONDS
            while True:
                try:
                    if time.time() > end_time:
                        break
                    wellness.append(pickle.loads(self._r.brpop(redisQueues.WELLNESS)[1]))
                    pollution.append(pickle.loads(self._r.brpop(redisQueues.POLLUTION)[1]))
                except Exception as e:
                    print(e)
            tstamp = pollution[len(pollution) - 1].timestamp
            dateString = datetime.datetime.fromtimestamp(tstamp.ToSeconds()).strftime('%H:%M:%S')
            result = proxy_pb2.Result(wellness=sum(wl.wellness for wl in wellness) / len(wellness),
                                      pollution=sum(pl.pollution for pl in pollution) / len(pollution),
                                      datetime=dateString)
            print(result)
            for terminal in self._terminals.keys():
                try:
                    self._terminals[terminal].SendResults(result)
                except Exception:
                    print("Terminal " + str(terminal) + " disconnected.")
                    self._terminals.pop(terminal)
                    self.tumblingWindow()

    def addTerminal(self, port):
        channel = grpc.insecure_channel('localhost:' + str(port))
        self._terminals[port] = proxy_pb2_grpc.ResultsServiceStub(channel)
        print("Added connection to terminal in port " + str(port))

    def serve(self):
        # listen on port 50055
        print('Starting Proxy server. Listening on port ' + str(self._serverPort) + ' for terminals to establish connection.')
        with futures.ThreadPoolExecutor(max_workers=10) as pool:
            self._server = grpc.server(pool)
            userTerminal_pb2_grpc.add_ConnectionTServiceServicer_to_server(
                ConnectionTServiceServicer(), self._server)
            try:
                self._server.add_insecure_port('[::]:' + str(self._serverPort))
                self._server.start()
                try:
                    self._server.wait_for_termination()
                except KeyboardInterrupt or Exception:
                    print("Server stopped.")
            except Exception as e:
                print("There is a problem with the port, maybe it is being used by other application.")
                print(e)


if __name__ == '__main__':
    p = Proxy()

    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(p.serve)
        executor.submit(p.tumblingWindow)
