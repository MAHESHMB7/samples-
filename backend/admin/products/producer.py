import pika, json

params = pika.URLParameters('amqp://guest:guest@host.docker.internal:5672?connection_attempts=10&retry_delay=10')


connection = pika.BlockingConnection(params)

channel = connection.channel()


# def publish():
    # channel.basic_publish(exchange='', routing_key='main', body=' hello main')



def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='main', body=json.dumps(body), properties=properties)
