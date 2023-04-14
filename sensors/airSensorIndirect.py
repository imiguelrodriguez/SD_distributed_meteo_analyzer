import datetime
import json
import sys
import time
import pika
import rabbitQueue
from meteo_utils import MeteoDataDetector

print("Running air sensor.")

try:

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitQueue.QUEUE)
    generator = MeteoDataDetector()
    while True:
        time.sleep(2)

        # obtain data
        timestamp = datetime.datetime.now().timestamp()
        data = generator.analyze_air()
        data["timestamp"] = timestamp
        # create a valid request message

        channel.basic_publish(exchange="",
                              routing_key=rabbitQueue.QUEUE,
                              body=json.dumps(data).encode('utf-8'))
        print(" [x] Sent " + data.__str__())
except Exception as e:
    print(e)
    connection.close()
    sys.exit(0)
