
import pika

print("Running pollution sensor.")


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="pollution_data")

channel.basic_publish(exchange="",
                      routing_key="pollution_data",
                      body="Hello World".encode())
print(" [x] Sent 'Hello World!'")

connection.close()
