import pymongo
import json

def insertFeed(digested_feed, database, collection, host, port):
	# Insert a digested feed JSON in MongoDB.
	client = pymongo.MongoClient("mongodb://" + host + ":" + port + "/")
	db = client[database]
	col = db[collection]
	col.insert_one(json.loads(digested_feed))

def getFeed(database, collection, host, port, start, num_docs, filter_keyword = "", filter_sentiment = ""):
	# Get previously inserted digested feed JSON.

	# DB connection parameters
	client = pymongo.MongoClient("mongodb://" + host + ":" + port + "/")
	db = client[database]
	col = db[collection]

	# Dictionary to construct query
	query = {}

	# Add to query when filter are not empty
	if filter_keyword != "":
		query["keyword"] = { "$regex" : filter_keyword }
	if filter_sentiment != "":
		query["sentiment"] = { "$regex" : filter_sentiment }

	# When start = 0, then just get the latest num_docs elements in the DB.
	if start == 0:
		docs = col.find(query).sort("_id", -1).limit(num_docs)
	else:
		# Add timestamp limit to query
		query["_id"] = { "$lt" : start }
		docs = col.find(query).sort("_id", -1).limit(num_docs)
	return docs