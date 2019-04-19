# RSSummarizer - A Smart RSS Feed Engine for the cloud

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/logo.png" width="250"></p>

This work is part of the final project for CS-498 CCA course at University of Illinois Urbana-Champaign.

RSSummarizer is an engine to digest RSS Feeds from popular public news sites (e.g. New York Times, BBC, CNN, etc.) and present them in a user friendly interface so the user can explore, search, and find interesting news.

Even though there are many RSS readers available, there is no a centralized place with digested and up-to-date news and articles from many different RSS feeds that allow consumers to easily explore instead of having to know the exact feed to subscribe to.

The implementation is based on cloud technologies. The engine fetches real-time data coming from many popular RSS news feeds URLs using data streaming technologies (Kafka) to publish the parsed feeds, run NLP Machine Learning models to do sentiment analysis and keyword extraction over the feed information, and finally store the digested and consolidated information in a noSQL database (MongoDB). The digested information is presented to the end user through a front-end (Flask and Bootstrap) with a search bar to find keywords or filter by sentiment.

## To be added (enhancements)

Here you can find a list of possible enhancements for this implementation:

1. Create a web scraper engine in charge of automatically populate the input file with more and more URL of news RSS Feeds.
2. Use a distributed architecture for MongoDB.
3. Consider using Apache Spark MLLib or similar to digest the pusblished feeds on Kafka. This would add fault-tolerance to the system from end-to-end.
4. Implement the whole system in the cloud.
5. Improve the module that compares the difference between RSS Feed XMLs to only publish new articles in case there are some repeated in the temporal files stored.
6. Add a smarter search engine to the front-end that allows you to use natural language queries to find relevant articles. Some filters can also be added to search by date, etc.
7. Add exception handling to all the code.

## Getting Started

All the instructions to run this engine on a local machine are provided here. Below you can find a high-level diagram which explain all the modules that compose RSSummarizer.

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/BlockHighLevelDiagram.png" width="400"></p>

Based on the numbers shown in the diagram, here is an explanation of each step and where to locate the source code:

1. This block is composed by 4 modules (all located in 'producer' directory: 
	* **feed_retriever.py**: read the list of RSS feed URLs (located in 'input' directory) and download the XML files related to those. The output is stored in a temporary directory.
	* **file_comparator.py**: compare previous XML downloaded from the same source and list all the differences so the new feeds can be published.
	* **kafka_producer.py**: parse the new feeds, and prepare a JSON output for each feed that is published to the Kafka stream.
	* **main_producer.py**: orchestrate and call the previous 3 modules to publish the RSS feeds to Kafka under a topic called 'rss'.

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
	* **nlp_feed_analysis.py**: subscribe to the Kafka stream and use Rake and Textblob to process the incoming JSON and generate the sentiment analysis and keyword extraction.
	* **feed_storage.py**: store and fetch the digested RSS feed from MongoDB.
	* **main_consumer.py**: orchestrate and call the previous 2 modules in order to read new RSS feeds coming from Kafka, apply the NLP analysis, and store the digested feed in the database.

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
	* **rss_feed_front_end.py**: Flask API to retrieve data from noSQL database. It has the following methods: 
		* GET / with optional parameters “sentiment” (to request a specific sentiment) and “keyword” (to request a specific keyword) as query strings.
		* GET /v1/get-articles with parameters “number” (to define the number of articles to fetch), “start” (to define the starting key to fetch), “sentiment” (to filter for a specific sentiment), and “keyword” (to filter for a specific keyword).

	* **index.html and styles** (located inside 'consumer/static' and 'consumer/templates' directories): this HTML uses Bootstrap and CSS to render the feeds as cards on the front-end. It also includes Ajax calls to fetch feeds on demand as the end user scrolls down instead of downloading everything.

### Prerequisites

This implementation has been tested on a local machine (Mac OS) using a combination of 3 main elements:

1. Python 3.X libraries
2. Kafka/Zookeeper Docker container
3. MongoDB

### Installing

Let's go over each of the components. The following instructions were tested on MacOS Mojave, but should work on any enviroment as long as all the pieces of software are installed.

1. Python 3.X libraries

	* Install Python 3 by following the instructions listed [here](https://docs.python-guide.org/starting/install3/osx/).
	* Even though it is not strictly necessary, it is highly recommended to use a virtual environment so you can have a clean environment to install only the required libraries to test RSSummarizer and avoid overlapping or 'polluting' your main environment. A nice tutorial can be found [here](https://realpython.com/python-virtual-environments-a-primer/).
	* Once your Python 3.X environment is ready you can proceed to install the dependencies. You can simply use the 'requirements.txt' file located in this repository as follows:
```
pip install -r requirements.txt
```

2. Kafka/Zookeeper Docker container

	* Download and install Docker Desktop from [here](https://www.docker.com/products/docker-desktop)
	* Download the Docker container (Kafka + Zookeper) as follows:
```
docker pull spotify/kafka
```
	* Once the image is downloaded, run this command to launch the instance:
```
docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=localhost --env ADVERTISED_PORT=9092 spotify/kafka
```

3. MongoDB

	* Install and run mongoDB by following the instructions [here](https://treehouse.github.io/installation-guides/mac/mongo-mac.html)
	* Once installed just run mongoDB deamon on the terminal:

```
$mongod
```

## Running the tests

To test the end-to-end implementation, follow these instructions:

1. Open a terminal and run mongoDB deamon `$mongodb`.
2. Open another terminal and run the Docker container as instructed in the previous section.
3. Open another terminal and run your Python virtual environment (in case you are using one as recommended). Go to the 'consumer' directory (`$cd consumer`) and execute the following command:

```
$python main_consumer.py
```

This will make your 'consumer' side to start listening for new published feeds through 'rss' topic on Kafka.

4. Open another terminal and run your Python virtual environment (in case you are using one as recommended). Go to the 'producer' directory (`$cd producer`) and execute the following commands:

```
$mkdir /tmp/kafka_output
$python main_producer.py ../input/rss_feeds_url.txt /tmp/kafka_output/
```

Notice that we are using "/tmp/kafka_output" to store the temporal XML files used to create the feeds. After running this command, a set of RSS Feed are parsed to JSON and published to Kafka. The output should be similar to the following:

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/main_producer_output.png" width="800"></p>

If you go back to the terminal where you executed the 'main_consumer.py' program you should see something like this:

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/main_consumer_output.png" width="800"></p>

This simply means that all the available RSS Feed JSONs published on Kafka have been consumed, digested, and stored in MongoDB.

In a production environment the idea is that 'main_producer.py' should be executed periodically (e.g. every 30 seconds) so the stream of RSS Feed JSONs will be continously pushed to the Kafka 'rss' topic. The bigger the list of RSS Feed URLs, the more intensive the stream will be.

5. Now you can start consuming the information stored on MongoDB by starting Flask API and the front-end. For this purpose we are using the embedded testing web server on Flask. Open another terminal and run your Python virtual environment (in case you are using one as recommended). Go to the 'consumer' directory (`$cd consumer`) and execute the following commands:

```
$python rss_feed_front_end.py
```

Open a browser and navigate to http://localhost:5000/. You'll get the web interface as follows:

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/front_end_view.png" width="800"></p>

If you scroll down, more cards will be loaded dynamically. If you click on any 'keyword' or 'sentiment' you'll filter a search based on those. Similarly, if you click on 'Link to the article' a new tab will be opened to the source of the article. You can also use the 'search bar' at the top right to look for a specific keyword or sentiment.

Here is an example of a filtered view on the keyword 'time':

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/filtered_front_end_view.png" width="800"></p>

## Deployment

This implementation was not deployed to any production environment. It should be easily migrated to a cloud environment that has all the components installed.

## Built With

RSSummarize is powered by several open-source components. The main ones are:

* [Apache Kafka](https://kafka.apache.org/)
* [Flask](http://flask.pocoo.org/)
* [MongoDB](https://www.mongodb.com/)
* [Python](https://www.python.org/)

## Authors

* **Francisco Vargas (fav3@illinois.edu)**
* **Hari Manan (nfnh2@illinois.edu)**
* **Victor Sosa (victors3@illinois.edu)**

## License

This is an open project as part of the learning experience of CS-498 CCA. Feel free to re-use the code, implement it, and enhance it under GNU v3 license. 

## Acknowledgments

Thanks to our instructors and TAs for all the support throughout the course.

Thanks to the open-source community for let us use such an amazing set of tools to build this concept.