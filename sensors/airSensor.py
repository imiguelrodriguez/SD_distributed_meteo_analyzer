import grpc
import airSensor_pb2
import airSensor_pb2_grpc
import rawTypes_pb2
from meteo_utils import MeteoDataDetector
import time
import datetime

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = airSensor_pb2_grpc.AirBalancingServiceStub(channel)

generator = MeteoDataDetector()
while True:
    time.sleep(2)

    # obtain data
    now = datetime.datetime.now()
    timestamp = rawTypes_pb2.google_dot_protobuf_dot_timestamp__pb2.Timestamp()
    timestamp.FromDatetime(now)
    data = generator.analyze_air()

    # create a valid request message
    message = rawTypes_pb2.RawMeteoData(temperature=data['temperature'], humidity=data['humidity'],
                                         datetime=timestamp)

    # send message
    stub.SendAirData(message)


