from confluent_kafka import Producer
import os
import datetime
import json
import xml.etree.ElementTree as ET

conf = {'bootstrap.servers': 'localhost:9092', 'client.id': 'rss'}
producer = Producer(conf)

ns = {
	'dc': 'http://purl.org/dc/elements/1.1/',
	'atom': 'http://www.w3.org/2005/Atom'
}

# Parse and publish all feeds from RSS feed XML files list
def process_feed_file(files):
	# Iterate over each XML file and publish
	for feed_file in files:
		# Only parse XML files
		if feed_file.endswith('.xml') is True:
			parse_xml_feed(feed_file)
		
# Parse independent RSS feed XML files and publish the feeds
def parse_xml_feed(feed_file):
	print("Pushing feed file: " + feed_file)
	tree = ET.parse(feed_file)
	channel_element = tree.getroot()[0]

	# Iterate over the RSS feed items which represents each article or post
	for feed_item in channel_element.iter('item'):
		# Extract author, description, title and URL of each article or post
		author = feed_item.find('dc:creator',ns).text if feed_item.find('dc:creator', ns) is not None else feed_item.find('author').text
		url = feed_item.find('atom:link', ns).attrib['href'] if feed_item.find('atom:link', ns) is not None else feed_item.find('link').text

		# Format them as JSON before publishing
		feed = {
			"title" : feed_item.find('title').text,
			"author" : author,
			"description" : feed_item.find('description').text,
			"url" : url
		}
		json_data = json.dumps(feed)
		now = datetime.datetime.now()
		timestamp = now.strftime("%Y%m%d%H%M%S%f")

		# Publish
		producer.produce(topic= 'rss', key=timestamp, value=json_data)

	# Clean producer object
	producer.flush()

