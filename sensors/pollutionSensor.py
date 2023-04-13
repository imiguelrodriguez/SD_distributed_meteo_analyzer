import sys

import grpc
import pollutionSensor_pb2
import pollutionSensor_pb2_grpc
from data import rawTypes_pb2
from meteo_utils import MeteoDataDetector
import time
import datetime

print("Running pollution sensor.")

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = pollutionSensor_pb2_grpc.PollutionBalancingServiceStub(channel)

generator = MeteoDataDetector()
while True:
    time.sleep(2)

    # obtain data
    now = datetime.datetime.now()
    timestamp = rawTypes_pb2.google_dot_protobuf_dot_timestamp__pb2.Timestamp()
    timestamp.FromDatetime(now)
    data = generator.analyze_pollution()

    # create a valid request message
    message = rawTypes_pb2.RawPollutionData(co2=int(data['co2']), datetime=timestamp)
    try:
        # send message
        stub.SendPollutionData(message)
    except Exception:
        print("Server stopped.")
        sys.exit(0)