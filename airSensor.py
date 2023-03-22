import grpc

import airSensor_pb2
import airSensor_pb2_grpc
from meteo_utils import MeteoDataDetector
import time
import datetime
from google.protobuf.timestamp_pb2 import Timestamp
timestamp = Timestamp()

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = airSensor_pb2_grpc.BalancingServiceStub(channel)

generator = MeteoDataDetector()
while True:
    time.sleep(2)

    # obtain data
    timestamp = datetime.datetime().now().timestamp()
    data = generator.analyze_air()

    # create a valid request message
    message = airSensor_pb2.RawMeteoData(temperature=data['temperature'], humidity=data['humidity'], timestamp=airSensor_pb2._timestamp_pb2)

    # send message
    stub.SendAirData(message)


