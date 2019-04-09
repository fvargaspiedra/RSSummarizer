#!/usr/bin/env python3

import os
from flask import Flask, render_template, request, json, jsonify
import feed_storage

# Initialize flask object
app = Flask(__name__)

# This route is used for the main page of the tool
@app.route('/', methods=['GET'])
def index():
	# Check if the request comes with a filter
	if request.args.get('sentiment'):
		sentiment_filter = request.args.get('sentiment').lower()
	else: 
		sentiment_filter = ""
	if request.args.get('keyword'):
		keyword_filter = request.args.get('keyword').lower()
	else: 
		keyword_filter = ""

	data = {"sentiment_filter" : sentiment_filter, "keyword_filter" : keyword_filter}
	return render_template('index.html', data = data)

@app.route('/v1/get-articles', methods=['GET'])
def get_articles():
	number_articles = request.args.get('number')
	start_key = request.args.get('start')
	sentiment_filter = request.args.get('sentiment')
	keyword_filter = request.args.get('keyword')

	# Get list of objects from MongoDB
	data = feed_storage.getFeed("rss_feed_db", "rss_feed", "localhost", "27017", float(start_key), int(number_articles), keyword_filter, sentiment_filter)

	# When there is no a result just respond with no-content (204)
	if not data:
		return ('', 204)

	return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)