import os
import sys
from concurrent import futures

import grpc
import redis
import pickle
import socket
import meteo_utils
import processingServer_pb2
import processingServer_pb2_grpc
import redisQueues
from lb import loadBalancer_pb2_grpc


class WellnessAux:
    def __init__(self, wellness, datetime):
        self.wellness = wellness
        self.timestamp = datetime


class PollutionAux:
    def __init__(self, pollution, datetime):
        self.pollution = pollution
        self.timestamp = datetime


class DataProcessingServicer(loadBalancer_pb2_grpc.DataProcessingServiceServicer):
    def __init__(self, ps):
        self._ps = ps
        self._connection = processingServer_pb2.Connection(port=self._ps.port)
        self._stub = processingServer_pb2_grpc.ConnectionServiceStub(self._ps.subscribeChannel)
        self._processor = meteo_utils.MeteoDataProcessor()
        self._r = redis.Redis(host="localhost", port=6379)

    def ProcessMeteoData(self, data, context):
        temperature = data.temperature
        humidity = data.humidity
        timestamp = data.datetime
        print(str(temperature) + " ", str(humidity) + " ", str(timestamp) + "")
        wellness = self._processor.process_meteo_data(data)
        print("wellness: " + str(wellness))
        wellness = WellnessAux(wellness=wellness, datetime=timestamp)
        wellness_pkl = pickle.dumps(wellness)
        try:
            self._r.lpush(redisQueues.WELLNESS, wellness_pkl)
        except Exception as e:
            print(e)
        return self._connection

    def ProcessPollutionData(self, data, context):
        co2 = data.co2
        timestamp = data.datetime
        print(str(co2) + " ", str(timestamp) + "")
        pollution = self._processor.process_pollution_data(data)
        print("pollution: " + str(pollution))
        pollution = PollutionAux(pollution=pollution, datetime=timestamp)
        pollution_pkl = pickle.dumps(pollution)
        try:
            self._r.lpush(redisQueues.POLLUTION, pollution_pkl)
        except Exception as e:
            print(e)
        return self._connection


class ProcessingServer:
    def __init__(self):
        self._server = None
        self._subscribeChannel = None
        sock = socket.socket()
        sock.bind(('', 0))
        self._port = sock.getsockname()[1]
        self.subscribeToLB()
        self.serve()

    def subscribeToLB(self):
        lbPort = ""
        try:
            with open(".." + os.sep + "lbServersPort.txt", "r") as f:
                lbPort = f.readline()
                f.close()
            # subscribe channel to send the chosen port to the LB
            self._subscribeChannel = grpc.insecure_channel('localhost:' + lbPort)
            connection = processingServer_pb2.Connection()
            connection.port = self._port
            print("Chosen port for server: " + str(self._port))
            stub = processingServer_pb2_grpc.ConnectionServiceStub(self._subscribeChannel)
            stub.SubscribeToLoadBalancer(connection)
        except Exception:
            print("Couldn't read LB port.")
            sys.exit(0)

    def serve(self):
        print('Starting Processing server. Listening on port ' + str(self._port))
        with futures.ThreadPoolExecutor(max_workers=10) as pool:
            self._server = grpc.server(pool)
            # to add the defined class to the server
            loadBalancer_pb2_grpc.add_DataProcessingServiceServicer_to_server(
                DataProcessingServicer(self), self._server)
            self._server.add_insecure_port('0.0.0.0:' + str(self._port))
            self._server.start()
            try:
                self._server.wait_for_termination()
            except KeyboardInterrupt or Exception:
                print("Server stopped.")

    @property
    def port(self):
        return self._port

    @property
    def subscribeChannel(self):
        return self._subscribeChannel


if __name__ == "__main__":
    ProcessingServer()
