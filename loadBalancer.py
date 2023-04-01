from queue import Queue

import grpc
from concurrent import futures

import loadBalancer_pb2_grpc
import processingServer_pb2
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
        response = processingServer_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response


class LoadBalancer:
    _lbSensorsPort = 50051
    _lbServersPort = 50052

    def __init__(self):
        self._dataQueue = Queue()
        self._servers = dict()  # this dictionary will store ports as keys and their correspondent stubs as values
        self._serversQueue = Queue()
        self._server = None

    def process_response(self, call_future):
        self._serversQueue.put(call_future.result().port)

    def distributeDataRR(self):
        print("Distributing data to servers...")
        while True:
            data = self._dataQueue.get(block=True)
            if isinstance(data, sensors.rawTypes_pb2.RawMeteoData):
                call_future = self._servers[self._serversQueue.get(block=True)].ProcessMeteoData.future(data)
                call_future.add_done_callback(self.process_response)
            else:
                call_future = self._servers[self._serversQueue.get(block=True)].ProcessPollutionData.future(data)
                call_future.add_done_callback(self.process_response)

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

            self._server.add_insecure_port('[::]:' + str(self._lbSensorsPort))
            self._server.add_insecure_port('[::]:' + str(self._lbServersPort))
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

    @property
    def serversQueue(self):
        return self._serversQueue

    @property
    def lbServersPort(self):
        return self._lbServersPort


if __name__ == '__main__':
    lb = LoadBalancer()

    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(lb.serve)
        executor.submit(lb.distributeDataRR)
