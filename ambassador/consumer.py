import django
import json
import os

from confluent_kafka import Consumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

# from core.models import KafkaError
import core.listeners

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

print('Start the ambassador consumer')
while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        continue

    print(msg.key())
    print(msg.key().decode('utf-8'))
    try:
        getattr(core.listeners, msg.key().decode('utf-8'))(json.loads(msg.value()))
    except Exception as e:
        # 教學目的，不會把錯存在MySQL
        # ELK or 其他解
        # KafkaError.objects.create(
        #     key=msg.key(),
        #     value=msg.value(),
        #     error=str(e),
        # )
        print('--------- error part ----------')
        print('listener: ', getattr(core.listeners, msg.key().decode('utf-8')))
        print('key: ', msg.key(), msg.key().decode('utf-8'))
        print('key: ', msg.value(), json.loads(msg.value()))
        print(f'error happened {str(e)}')

consumer.close()
