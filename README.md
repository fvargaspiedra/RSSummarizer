# RSSummarizer - A Smart RSS Feed Engine for the cloud

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/logo.png" width="250"></p>

This work is part of the final project for CS-498 CCA course at University of Illinois Urbana-Champaign.

RSSummarizer is an engine to digest RSS Feeds from popular public news sites (e.g. New York Times, BBC, CNN, etc.) and present them in a user friendly interface so the user can explore, search, and find interesting news.

Even though there are many RSS readers available, there is no a centralized place with digested and up-to-date news and articles from many different RSS feeds that allow consumers to easily explore instead of having to know the exact feed to subscribe to.

The implementation is based on cloud technologies. The engine fetches real-time data coming from many popular RSS news feeds URLs using data streaming technologies (Kafka) to publish the parsed feeds, run NLP Machine Learning models to do sentiment analysis and keyword extraction over the feed information, and finally store the digested and consolidated information in a noSQL database (MongoDB). The digested information is presented to the end user through a front-end (Flask and Bootstrap) with a search bar to find keywords or filter by sentiment.

## To be added

TBD

## Getting Started

All the instructions to run this engine on a local machine are provided here. Below you can find a high-level diagram which explain all the modules that compose RSSummarizer.

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/BlockHighLevelDiagram.png" width="400"></p>

Based on the numbers shown in the diagram, here is an explanation of each step and where to locate the source code:

1. This block is composed by 4 modules (all located in 'producer' directory: 
	* feed_retriever.py: read the list of RSS feed URLs (located in 'input' directory) and download the XML files related to those. The output is stored in a temporary directory.
	* file_comparator.py: compare previous XML downloaded from the same source and list all the differences so the new feeds can be published.
	* kafka_producer.py: parse the new feeds, and prepare a JSON output for each feed that is published to the Kafka stream.
	* main_producer.py: orchestrate and call the previous 3 modules to publish the RSS feeds to Kafka under a topic called 'rss'.

2. Each feed is published to the Kafka topic “rss” using the following JSON format:

```
{
   "title": "Foo",
   "author": "John Doe",
   "description": "Lorem Ipsum.",
   "url": "example.com/bar" 
}
```

3. This block is composed by 3 modules (all located in 'consumer' directory):
	* nlp_feed_analysis.py: subscribe to the Kafka stream and use Rake and Textblob to process the incoming JSON and generate the sentiment analysis and keyword extraction.
	* feed_storage.py: store and fetch the digested RSS feed from MongoDB.
	* main_consumer.py: orchestrate and call the previous 2 modules in order to read new RSS feeds coming from Kafka, apply the NLP analysis, and store the digested feed in the database.

4. The digested JSONs stored in MongoDB have the following structure (notice that the ID corresponds to the timestamp including miliseconds):

```
{
   "_id": "1555550489.283562"
   "title": "Foo",
   "author": "John Doe",
   "description": "Lorem Ipsum.",
   "url": "example.com/bar",
   "sentiment": ["foo","bar"],
   "keyword": ["Lorem"],
}
```

5. This block is composed by 2 elements (all located in 'consumer' directory):
	* rss_feed_front_end.py: Flask API to retrieve data from noSQL database. It has the following methods: 
		* GET / with optional parameters “sentiment” (to request a specific sentiment) and “keyword” (to request a specific keyword) as query strings.
		* GET /v1/get-articles with parameters “number” (to define the number of articles to fetch), “start” (to define the starting key to fetch), “sentiment” (to filter for a specific sentiment), and “keyword” (to filter for a specific keyword).

	* index.html and styles (located inside 'consumer/static' and 'consumer/templates' directories): this HTML uses Bootstrap and CSS to render the feeds as cards on the front-end. It also includes Ajax calls to fetch feeds on demand as the end user scrolls down instead of downloading everything.

### Prerequisites

TBD

### Installing

TBD

## Running the tests

TBD

## Deployment

TBD

## Built With

TBD

## Versioning

## Authors

* **Francisco Vargas (fav3@illinois.edu)**
* **Hari Manan (nfnh2@illinois.edu)**
* **Victor Sosa (victors3@illinois.edu)**

## License

TBD

## Acknowledgments

TBD