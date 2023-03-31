from queue import Queue

import grpc
from concurrent import futures

import loadBalancer_pb2_grpc
import sensors.rawTypes_pb2
from sensors import airSensor_pb2_grpc, pollutionSensor_pb2_grpc, airSensor_pb2, pollutionSensor_pb2
import processingServer_pb2_grpc


class LoadBalancerAirServicer(airSensor_pb2_grpc.AirBalancingServiceServicer):
    def SendAirData(self, data, context):
        temperature = data.temperature
        humidity = data.humidity
        timestamp = data.datetime
        print(str(temperature) + " ", str(humidity) + " ", str(timestamp) + "")
        print("TYPE: " + str(type(data)))
        lb.dataQueue.put(data)
        response = airSensor_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class LoadBalancerPollutionServicer(pollutionSensor_pb2_grpc.PollutionBalancingServiceServicer):
    def SendPollutionData(self, data, context):
        co2 = data.co2
        timestamp = data.datetime
        print(str(co2) + " ", str(timestamp) + "")
        lb.dataQueue.put(data)
        response = pollutionSensor_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class ConnectionServiceServicer(processingServer_pb2_grpc.ConnectionServiceServicer):
    def SubscribeToLoadBalancer(self, connection, context):
        port = connection.port
        lb.addServer(port)
        response = pollutionSensor_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class LoadBalancer:
    def __init__(self):
        self._dataQueue = Queue()
        self._servers = dict()  # this dictionary will store ports as keys and their correspondent stubs as values
        self._serversQueue = Queue()
        self._server = None

    def distributeDataRR(self):
        print("Distributing data to servers...")

        data = self._dataQueue.get(block=True)
        if isinstance(data, sensors.rawTypes_pb2.RawMeteoData):
            self._servers[self._serversQueue.get(block=True)].ProcessMeteoData(data)
        else:
            self._servers[self._serversQueue.get(block=True)].ProcessPollutionData(data)

    def serve(self):
        # listen on port 50051
        print('Starting Load Balancer server. Listening on port 50051 for sensors.')
        with futures.ThreadPoolExecutor(max_workers=10) as pool:
            self._server = grpc.server(pool)

            airSensor_pb2_grpc.add_AirBalancingServiceServicer_to_server(
                LoadBalancerAirServicer(), self._server)
            pollutionSensor_pb2_grpc.add_PollutionBalancingServiceServicer_to_server(
                LoadBalancerPollutionServicer(), self._server)
            processingServer_pb2_grpc.add_ConnectionServiceServicer_to_server(
                ConnectionServiceServicer(), self._server)

            self._server.add_insecure_port('[::]:50051')
            self._server.add_insecure_port('[::]:50052')
            print('Listening on port 50052 for new processing servers connection establishing.')
            self._server.start()
            try:
                self._server.wait_for_termination()
            except KeyboardInterrupt or Exception:
                print("Server stopped.")

    def addServer(self, port):
        channel = grpc.insecure_channel('localhost:' + str(port))
        self._servers[port] = loadBalancer_pb2_grpc.DataProcessingServiceStub(channel)
        self._serversQueue.put(port)

        print("Added connection to server in port " + str(port))

    @property
    def dataQueue(self):
        return self._dataQueue


lb = LoadBalancer()

with futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(lb.serve)
    executor.submit(lb.distributeDataRR)
