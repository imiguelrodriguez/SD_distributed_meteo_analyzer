# tiene que tener las dos llamadas send air y send pollution (como el insulting service)
import grpc
from concurrent import futures
import time
import airSensor_pb2
import airSensor_pb2_grpc

class LoadBalancerAirServicer(airSensor_pb2_grpc.BalancingServiceServicer):
    def __init__(self):
        pass

    def sendAirData(self, data):
        pass


class LoadBalancerPollutionServicer(airSensor_pb2_grpc.BalancingServiceServicer):
    def __init__(self):
        pass

    def sendPollutionData(self, data):
        pass




    def AddInsult(self, insult, context):
        insulting_service.add_insult(insult.insult, insult.severity)
        response = insultingServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response

    def GetInsults(self, empty, context):
        insults = insulting_service.get_insults()
        response = insultingServer_pb2.Insults()
        response.value.extend(insults)
        return response

    def InsultMe(self, empty, context):
        insult = insulting_service.insult_me()
        response = insultingServer_pb2.InsultName()
        response.insult = insult
        return response

    def GetSeverity(self, insult_name, context):
        insult_name = insult_name.insult
        severity = insulting_service.get_severity(insult_name)
        response = insultingServer_pb2.Severity()
        response.severity = severity
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
insultingServer_pb2_grpc.add_InsultingServiceServicer_to_server(
    InsultingServiceServicer(), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('0.0.0.0:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
