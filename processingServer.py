import time

import grpc
from concurrent import futures

# create a gRPC server
import loadBalancer_pb2_grpc
import processingServer_pb2
import processingServer_pb2_grpc


class DataProcessingServicer(loadBalancer_pb2_grpc.DataProcessingServiceServicer):
    def ProcessMeteoData(self, data, context):
        pass

    def ProcessPollutionData(self, data, context):
        pass


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
loadBalancer_pb2_grpc.add_DataProcessingServiceServicer_to_server(
    DataProcessingServicer(), server)

# subscribe channel to send the chosen port to the LB
subscribe_channel = grpc.insecure_channel('localhost:50052')

import socket
sock = socket.socket()
sock.bind(('', 0))
port = sock.getsockname()[1]

connection = processingServer_pb2.Connection()
connection.port = port
print("Chosen port for server: " + str(port))
stub = processingServer_pb2_grpc.ConnectionServiceStub(subscribe_channel)
stub.SubscribeToLoadBalancer(connection)

# listen on free random port
print('Starting Processing server. Listening on port ' + str(port))

server.add_insecure_port('0.0.0.0:' + str(port))

server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    server.wait_for_termination()
except KeyboardInterrupt:
    print("Server stopped.")