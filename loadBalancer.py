import grpc
from concurrent import futures
import time
import airSensor_pb2
import airSensor_pb2_grpc
import pollutionSensor_pb2_grpc


class LoadBalancer:
    def __init__(self):
        pass

    def distributeDataRR(self):
        print()


class LoadBalancerAirServicer(airSensor_pb2_grpc.AirBalancingServiceServicer):
    def SendAirData(self, data, context):
        temperature = data.temperature
        humidity = data.humidity
        timestamp = data.datetime
        print(str(temperature) + " ", str(humidity) + " ", str(timestamp) + "")
        response = airSensor_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class LoadBalancerPollutionServicer(pollutionSensor_pb2_grpc.PollutionBalancingServiceServicer):
    def SendPollutionData(self, data, context):
        co2 = data.co2
        timestamp = data.datetime
        print(str(co2) + " ", str(timestamp) + "")
        response = airSensor_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
airSensor_pb2_grpc.add_AirBalancingServiceServicer_to_server(
    LoadBalancerAirServicer(), server)
pollutionSensor_pb2_grpc.add_PollutionBalancingServiceServicer_to_server(
    LoadBalancerPollutionServicer(), server)

# listen on port 50051
print('Starting Load Balancer server. Listening on port 50051.')
server.add_insecure_port('0.0.0.0:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
