#! /usr/bin/python

from confluent_kafka import Consumer
import nlp_feed_analysis
import feed_storage

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

    digested_feed = nlp_feed_analysis.parseJSON(msg.value())
    feed_storage.insertFeed(digested_feed, "rss_feed_db", "rss_feed", "localhost", "27017")

c.close()