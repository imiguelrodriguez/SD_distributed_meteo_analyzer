import pika

print("Running air sensor.")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="meteo_data")

channel.basic_publish(exchange="",
                      routing_key="meteo_data",
                      body="Hello World".encode())
print(" [x] Sent 'Hello World!'")

connection.close()
