# RSSummarizer - An RSS News Feed digester on the cloud

<p align="center"><img src="https://github.com/fvargaspiedra/RSSummarizer/blob/master/misc/logo.png" width="200"></p>

This work is part of the final project for CS-498 CCA course at University of Illinois Urbana-Champaign.

RSSummarizer is an engine to digest RSS Feeds from popular public news sites (e.g. New York Times, BBC, CNN, etc.) and present them in a user friendly interface so the user can explore, search, and find interesting news.

Even though there are many RSS readers available, there is no a centralized place with digested and up-to-date news and articles from many different RSS feeds that allow consumers to easily explore instead of having to know the exact feed to subscribe to.

The implementation is based on cloud technologies. The engine fetches real-time data coming from many popular RSS news feeds URLs using data streaming technologies (Kafka) to publish the parsed feeds, run NLP Machine Learning models to do sentiment analysis and keyword extraction over the feed information, and finally store the digested and consolidated information in a noSQL database (MongoDB). The digested information is presented to the end user through a front-end (Flask and Bootstrap) with a search bar to find keywords or filter by sentiment.

## To be added

TBD

## Getting Started

All the instructions to run this engine on a local machine are provided here. 

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