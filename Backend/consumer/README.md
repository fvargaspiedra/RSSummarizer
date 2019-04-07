# nlp-digest-rss-feed-engine

This work is part of CS-498 CCA course at University of Illinois.

The module gets a simple JSON with information related to an RSS feed and adds a unique ID (timestamp), sentiment based on the description of the RSS Feed (neutral, positive, or negative), and a lit of keywords based on the description of the RSS Feed.

The JSON input format has the following structure:

```
{
  "title": "3 Questions: Why are student-athletes amateurs?",
  "author": "Peter Dizikes | MIT News Office",
  "description": "MIT Professor Jennifer Light digs into the history of the idea that students aren\u2019t part of the labor force.",
  "url": "http://news.mit.edu/2019/jennifer-light-student-athletes-0325"
}
```

Once the JSON RSS Feed data is parsed by using Rake (for keyword extraction) and TextBlob (for sentiment analysis) the output will look as follows:

```
{
  "title": "3 Questions: Why are student-athletes amateurs?",
  "author": "Peter Dizikes | MIT News Office",
  "description": "MIT Professor Jennifer Light digs into the history of the idea that students aren\u2019t part of the labor force.",
  "url": "http://news.mit.edu/2019/jennifer-light-student-athletes-0325",
  "key": 1554673646.549649,
  "sentiment": "positive",
  "keyword": [
    "mit professor jennifer light digs",
    "labor force",
    "students"
  ]
}
```

# Development and testing

The module expects a JSON with the input structure shown in the previous section. The output will be stored in a noSQL database to be used by the front-end.

# Authors

* **Francisco Vargas (fav3@illinois.edu)**
* **Hari Manan (nfnh2@illinois.edu)**
* **Victor Sosa (victors3@illinois.edu)**