import pika, json

from main import product, db

params = pika.URLParameters('amqp://guest:guest@host.docker.internal:5672?connection_attempts=10&retry_delay=10')
# params = pika.URLParameters('amqp://guest:guest@host.docker.internal:5672/%2F')
# params = pika.URLParameters('amqp://guest:guest@host.docker.internal:5672')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'product_created':
        Product = product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(Product)
        db.session.commit()
        print('Product Created')

    elif properties.content_type == 'product_updated':
        Product = product.query.get(data['id'])
        Product.title = data['title']
        Product.image = data['image']
        db.session.commit()
        print('Product Updated')

    elif properties.content_type == 'product_deleted':
        Product = product.query.get(data)
        db.session.delete(Product)
        db.session.commit()
        print('Product Deleted')


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
