#! /usr/bin/python

import sys
import feed_retriever
import file_comparator
import kafka_producer
import argparse

# Two arguments are expected, the file with the list of RSS feed URLs and the output directory
# to store downloaded RSS feed XML files.
argparser = argparse.ArgumentParser(description = 'Download, parse, and publish RSS feeds to Kafka')
argparser.add_argument("rss_url_file",
                        help="Path to file with list of RSS feed URLs to connect to.", type=str)
argparser.add_argument("output_directory",
                       help="Path to directory to store downloaded RSS feed XML files.", type=str)
args = argparser.parse_args()

# Save arguments in variables
rss_file_location = args.rss_url_file
output_directory = args.output_directory

# Add trailing slash if output directory doesn't have it
if output_directory.endswith('/') is False:
	output_directory = output_directory + "/"

# Read, download and store RSS feed XMLs based on list of RSS feed URLs
feed_retriever.read_rss_file(rss_file_location, output_directory)

# Get list of RSS feed XML files that have changed compared to previous
# downloaded XML of the same source
files_found = file_comparator.exec_find_files(output_directory)

# Publish feeds from RSS feed XML files that changed or are new
kafka_producer.process_feed_file(files_found)
