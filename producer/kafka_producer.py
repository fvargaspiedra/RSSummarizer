from confluent_kafka import Producer
import os
import datetime
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup 

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
		if feed_item.find('author') is not None:
			author = feed_item.find('author').text
		else:
			author = "Not specified"

		if feed_item.find('link') is not None:
			url = feed_item.find('link').text
		else: 
			# Not having a URL is unacceptable
			continue

		if feed_item.find('title') is not None:
			title = feed_item.find('title').text
		else: 
			# Not having a title is unacceptable
			continue	

		if feed_item.find('description') is not None:
			description = feed_item.find('description').text
			# Sometimes the description is empty, make sure that's not the case
			if description is not None:
				# Clean description in case it comes with images or external links as we only want plain text
				description = BeautifulSoup(description, "lxml").text
			else:
				continue
		else: 
			# Not having a description is unacceptable
			continue

		# Format them as JSON before publishing
		feed = {
			"title" : title,
			"author" : author,
			"description" : description,
			"url" : url
		}
		json_data = json.dumps(feed)
		now = datetime.datetime.now()
		timestamp = now.strftime("%Y%m%d%H%M%S%f")

		# Publish
		producer.produce(topic= 'rss', key = timestamp, value = json_data)

	# Clean producer object
	producer.flush()

