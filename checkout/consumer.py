import django
import json
import os

from confluent_kafka import Consumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

import core.listeners

consumer = Consumer({
    'bootstrap.servers': 'pkc-l7j7w.asia-east1.gcp.confluent.cloud:9092',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'EWGW6CHWHXQ6M2I3',
    'sasl.password': 'lBYnFyIMYAjqtrOrdZA7THC0EYKafF2bc7kX5mjPMzy8+G7qy6KthRyOYXHidy91',
    'sasl.mechanism': 'PLAIN',
    'group.id': 'myGroup',
    'auto.offset.reset': 'earliest',
})

consumer.subscribe(['checkout_topic'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print(f'Consumer error: {msg.error()}')
        continue

    # !!!!!! NOTE THIS !!!!!!!
    print(msg.key())
    print(msg.key().decode('utf-8'))
    try:
        print('lllll', json.loads(msg.value()))
        getattr(core.listeners, msg.key().decode('utf-8'))(json.loads(msg.value()))
    except Exception as e:
        print(str(e))

consumer.close()
