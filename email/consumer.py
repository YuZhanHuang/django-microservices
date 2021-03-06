import django
import json
import os

from confluent_kafka import Consumer
from django.core.mail import send_mail

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

consumer = Consumer({
    'bootstrap.servers': os.getenv('BOOTSTRAP_SERVICE'),
    'security.protocol': os.getenv('SECURITY_PROTOCOL'),
    'sasl.username': os.getenv('SASL_USERNAME'),
    'sasl.password': os.getenv('SASL_PASSWORD'),
    'sasl.mechanism': os.getenv('SASL_MECHANISMS'),
    'group.id': os.getenv('GROUP_ID'),
    'auto.offset.reset': 'earliest',
})

consumer.subscribe([os.getenv('KAFKA_TOPIC')])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        continue

    print("Received message: {}".format(msg.value()))
    order = json.loads(msg.value())

    send_mail(
        subject='An Order has been completed',
        message='Order #' + str(order['id']) + 'with a total of $' + str(
            order.get('admin_revenue')) + ' has been completed!',
        from_email='from@email.com',
        recipient_list=['admin@admin.com']
    )

    send_mail(
        subject='An Order has been completed',
        message='You earned $' + str(order.get('ambassador_revenue')) +
                ' from the link #' + order['code'],
        from_email='from@email.com',
        recipient_list=[order.get('ambassador_email')]
    )

consumer.close()
