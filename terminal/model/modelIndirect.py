import datetime
import pickle
import sys
from concurrent import futures

import pika
from queue import Queue
from terminal.controller.controller import Controller


class Result:
    def __init__(self, wellness, pollution, timestamp):
        self.wellness = wellness
        self.pollution = pollution
        self.datetime = timestamp

    def __str__(self):
        return f"Wellness: {self.wellness} Pollution: {self.pollution} Timestamp: {self.datetime}"


class Terminal:
    def __init__(self):
        self._resultsQueue = Queue()
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self._channel = self._connection.channel()

        self._channel.exchange_declare(exchange='logs', exchange_type='fanout')

        result = self._channel.queue_declare(queue='', exclusive=True)
        self._queue_name = result.method.queue

        self._channel.queue_bind(exchange='logs', queue=self._queue_name)

        print(' [*] Waiting for logs. To exit press CTRL+C')

        self._channel.basic_consume(
            queue=self._queue_name, on_message_callback=self.callback, auto_ack=True)

    def consume(self):
        self._channel.start_consuming()

    def callback(self, ch, method, properties, body):
        result = pickle.loads(body)
        result.datetime = datetime.datetime.fromtimestamp(result.datetime).strftime('%H:%M:%S')
        print(" [x] %r" % result.__str__())
        self._resultsQueue.put(result)

    def endTerminal(self):
        self._channel.close()
        self._connection.close()
        executor.shutdown(wait=False)
        sys.exit()

    @property
    def resultsQueue(self):
        return self._resultsQueue


if __name__ == '__main__':
    t = Terminal()
    controller = Controller(model=t)
    view = controller.createWindow()
    view.setController(controller)
    executor = futures.ThreadPoolExecutor(max_workers=1)
    executor.submit(t.consume)
    controller.runWindow()
