import json
import os
import pickle

import pika
import sys

import redis

import meteo_utils
import rabbitQueue
import redisQueues


class RawMeteoData:
    def __init__(self, temperature, humidity, datetime):
        self.temperature = temperature
        self.humidity = humidity
        self.timestamp = datetime


class RawPollutionData:
    def __init__(self, co2, datetime):
        self.co2 = co2
        self.timestamp = datetime


class WellnessAux:
    def __init__(self, wellness, datetime):
        self.wellness = wellness
        self.timestamp = datetime


class PollutionAux:
    def __init__(self, pollution, datetime):
        self.pollution = pollution
        self.timestamp = datetime


class ProcessingServer:
    def __init__(self):
        self._processor = meteo_utils.MeteoDataProcessor()
        try:
            self._r = redis.Redis(host="localhost", port=6379)
        except Exception as ex:
            print("Error while connecting to Redis.")
            print(ex)
            sys.exit(-1)

    def ProcessMeteoData(self, data):
        temperature = data.temperature
        humidity = data.humidity
        timestamp = data.timestamp
        print(str(temperature) + " ", str(humidity) + " ", str(timestamp) + "")
        wellness = self._processor.process_meteo_data(data)
        print("wellness: " + str(wellness))
        wellness = WellnessAux(wellness=wellness, datetime=timestamp)
        wellness_pkl = pickle.dumps(wellness)
        try:
            self._r.lpush(redisQueues.WELLNESS, wellness_pkl)
        except Exception as e:
            print(e)

    def ProcessPollutionData(self, data):
        co2 = data.co2
        timestamp = data.timestamp
        print(str(co2) + " ", str(timestamp) + "")
        pollution = self._processor.process_pollution_data(data)
        print("pollution: " + str(pollution))
        pollution = PollutionAux(pollution=pollution, datetime=timestamp)
        pollution_pkl = pickle.dumps(pollution)
        try:
            self._r.lpush(redisQueues.POLLUTION, pollution_pkl)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue=rabbitQueue.QUEUE)
        ps = ProcessingServer()


        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body.decode())
            data = json.loads(body.decode())
            if "co2" in data.keys():
                ps.ProcessPollutionData(RawPollutionData(data["co2"], data["timestamp"]))
            else:
                ps.ProcessMeteoData(RawMeteoData(data["temperature"], data["humidity"], data["timestamp"]))
            print(" [x] Done")


        channel.basic_consume(queue=rabbitQueue.QUEUE, on_message_callback=callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()


    except Exception as e:
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
