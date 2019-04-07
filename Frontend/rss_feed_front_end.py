import os
from flask import Flask, render_template, request, json, jsonify

# Initialize flask object
app = Flask(__name__)

# This route is used for the main page of the tool
@app.route('/', methods=['GET'])
def index():
	# Check if the request comes with a filter
	if request.args.get('sentiment'):
		sentiment_filter = request.args.get('sentiment').lower()
	else: 
		sentiment_filter = "all"
	if request.args.get('keyword'):
		keyword_filter = request.args.get('keyword').lower()
	else: 
		keyword_filter = "all"

	data = {"sentiment_filter" : sentiment_filter, "keyword_filter" : keyword_filter}
	return render_template('index.html', data = data)

@app.route('/v1/get-articles', methods=['GET'])
def get_articles():
	number_articles = request.args.get('number')
	start_key = request.args.get('start')
	sentiment_filter = request.args.get('sentiment')
	keyword_filter = request.args.get('keyword')
	print(number_articles)
	print(start_key)
	print(sentiment_filter)
	print(keyword_filter)

	# Default start_key of 0 is used to retrieve the latest N articles
	if start_key == 0:
		# Retrieve latest number_articles from DB
		print("dummy")
	else:
		# Retrieve the latest number_articles after start_key from DB
		print("dummy")

	# TBD When no new data is available, then respond with a 204.

	# Read dummy static JSON for response temporarily
	SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
	json_url = os.path.join(SITE_ROOT, "static/", "sample.json")
	data = json.load(open(json_url))
	return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)