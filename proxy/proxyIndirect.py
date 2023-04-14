import os
import pickle
import sys
import time
from concurrent import futures

import pika
import redis

import proxy_pb2

import redisQueues


class WellnessAux:
    def __init__(self, wellness, datetime):
        self.wellness = wellness
        self.timestamp = datetime

    def __str__(self):
        return "Wellness: " + str(self.wellness) + " Timestamp: " + str(self.timestamp)


class PollutionAux:
    def __init__(self, pollution, datetime):
        self.pollution = pollution
        self.timestamp = datetime

    def __str__(self):
        return "Pollution: " + str(self.pollution) + " Timestamp: " + str(self.timestamp)


class Result:
    def __init__(self, wellness, pollution, timestamp):
        self.wellness = wellness
        self.pollution = pollution
        self.timestamp = timestamp

    def __str__(self):
        return f"Wellness: {self.wellness} Pollution: {self.pollution} Timestamp: {self.timestamp}"


class Proxy:
    MAX_SECONDS = 4
    print("Running proxy.")

    def __init__(self):
        try:
            self._r = redis.Redis(host="localhost", port=6379)
        except Exception as e:
            print("There is a problem when connecting to the REDIS server.")
            print(e)
            sys.exit(-1)
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self._channel = self._connection.channel()
        self._channel.exchange_declare(exchange='logs', exchange_type='fanout')
        self.tumblingWindow()
        self._connection.close()

    def tumblingWindow(self):
        while True:
            wellness = []
            pollution = []
            end_time = time.time() + self.MAX_SECONDS
            while True:
                try:
                    if time.time() > end_time:
                        break
                    wellness.append(pickle.loads(self._r.brpop(redisQueues.WELLNESS)[1]))
                    pollution.append(pickle.loads(self._r.brpop(redisQueues.POLLUTION)[1]))
                except Exception as e:
                    print(e)
            tstamp = pollution[len(pollution) - 1].timestamp
            result = Result(wellness=sum(wl.wellness for wl in wellness) / len(wellness),
                            pollution=sum(pl.pollution for pl in pollution) / len(pollution),
                            timestamp=tstamp)
            print(result)
            self._channel.basic_publish(exchange='logs', routing_key='', body=pickle.dumps(result))
            print(" [x] Sent %r" % result)


if __name__ == '__main__':
    p = Proxy()
