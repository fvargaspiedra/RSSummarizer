import re
import datetime
import requests

# Read, download, and store a list of RSS feed URLs
def read_rss_file(rss_file_location, output_directory):
	# Read file with list of RSS feeds URLs
	rss_file = open(rss_file_location, "r")

	# Prepare suffix with date to save files
	now = datetime.datetime.now()
	suffix = now.strftime("_%Y%m%d%H%M%S.xml")

	# Iterate over all the RSS Feed URLs
	for rss in rss_file:
		rss = rss.strip()

		# Simple verification for malformed lines
		if len(rss) <= 1:
			continue

		# Filename will include parts of the URL plus the date suffix
		filename = re.compile("http://|https://").split(rss)[1]
		last_dot_index = filename.rfind(".")
		filename = filename[:last_dot_index]
		filename = re.sub("\.|\/", "_", filename)
		filename = filename + suffix

		# Download XML file from RSS feed URL and save it
		download_rss(rss, filename, output_directory)

# Download, and store a list of RSS feed URLs
def download_rss(url, filename, output_directory):
	print("Downloading content from " + url)
	print("Creating local file " + output_directory + filename)

	# Fetch XML from RSS feed URL and save it
	response = requests.get(url)

	# Use right encoding to avoid issues
	response.encoding = "utf-8-sig"

	# Only write output if response is a 200
	if response.status_code is 200:
		with open(output_directory + filename, 'w') as f:
			f.write(response.text)

