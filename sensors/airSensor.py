import os
import sys

import grpc
import airSensor_pb2_grpc
from data import rawTypes_pb2
from meteo_utils import MeteoDataDetector
import time
import datetime

print("Running air sensor.")
# open a gRPC channel
try:
    with open(".." + os.sep + "lbSensorsPort.txt", "r") as f:
        lbPort = f.readline()
        f.close()

    channel = grpc.insecure_channel('localhost:' + lbPort)

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
        try:
            # send message
            stub.SendAirData(message)
        except Exception:
            print("Server stopped.")
            sys.exit(0)
except Exception:
    print("Air sensor couldn't read LB port.")
    sys.exit(0)
