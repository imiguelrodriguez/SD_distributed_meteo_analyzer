import time

import grpc
from concurrent import futures
import socket

import loadBalancer_pb2
import loadBalancer_pb2_grpc
import processingServer_pb2
import processingServer_pb2_grpc


class DataProcessingServicer(loadBalancer_pb2_grpc.DataProcessingServiceServicer):
    def __init__(self, ps):
        self._ps = ps
        self._connection = processingServer_pb2.Connection(port=self._ps.port)
        self._stub = processingServer_pb2_grpc.ConnectionServiceStub(self._ps.subscribeChannel)

    def ProcessMeteoData(self, data, context):
        temperature = data.temperature
        humidity = data.humidity
        timestamp = data.datetime
        print(str(temperature) + " ", str(humidity) + " ", str(timestamp) + "")
        time.sleep(4)
        self._stub.FreeServer(self._connection)
        response = loadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def ProcessPollutionData(self, data, context):
        co2 = data.co2
        timestamp = data.datetime
        print(str(co2) + " ", str(timestamp) + "")
        time.sleep(4)
        self._stub.FreeServer(self._connection)
        response = loadBalancer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


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
        # subscribe channel to send the chosen port to the LB
        self._subscribeChannel = grpc.insecure_channel('localhost:50052')
        connection = processingServer_pb2.Connection()
        connection.port = self._port
        print("Chosen port for server: " + str(self._port))
        stub = processingServer_pb2_grpc.ConnectionServiceStub(self._subscribeChannel)
        stub.SubscribeToLoadBalancer(connection)

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


ProcessingServer()
