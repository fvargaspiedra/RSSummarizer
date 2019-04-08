#! /usr/bin/python

from confluent_kafka import Consumer
import nlp_feed_analysis

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'rss_group',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['rss'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    new_digested_feed = nlp_feed_analysis.parseJSON(msg.value())
    print(new_digested_feed)

c.close()