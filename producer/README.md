# feed-parser-kafka
Syndication feed retriever and parser that processes information using Apache Kafka

This application is split into 3 components, each in charge of one single task:
1. Retrieve the latest feed from a list of URL feeds and store the contents of each in a local file
2. Read each file and find differences. If there's any new feed, then the file will be processed next. If not, the file will be droped from the execution.
3. A Kafka producer that reads each of the diff'ed files and sends an event to a Kafka stream. 

This work is part of CS-498 CCA course at University of Illinois.

## Main
The whole program is executed by the *main* script. This script takes two input parameters:
* The input file with the list of URL to retrieve the feeds.
* The output directory where the feed files will be placed temporarily.

Both arguments are required.

```$ ./main.py <input file> <output directory>```

For instance:

```$ ./main.py ../input/rss_feeds_url.txt ../../output```

Note that the input supports full and relative paths.
A sample input file is included here in the *input* directory
## Feed retriever
The feed retrieval is done by script *feed_retriever*. This script will read the input file. This input file must have a single URL per line. The script will download the content of that URL feed into a local file with this name convention *url_timestamp.xml*. For instance, the URL *https://lb.webservices.illinois.edu/rss/19/text.xml* will produce a file named
*lb_webservices_illinois_edu_rss_19_text_20190321130923.xml* in the specified output.
## File comparator
Once the files are downloaded in local storage, the file comparator will search for each of those files and will compare them looking for differences, if there are no differences, then such file will not be added to the execution chain. The steps are as follows:
1. It will look at the file names and group them together in a sorted list.
2.  The list of grouped files, those with similar names, will be read and the contents compared with each other. If there's any difference between them, the newest file will be added to the execution chain.
3. It will pick the newest file based on the timestamp in the name deleting the old ones. This ensures that for each feed provider there's only one "old" file and whenever the execution starts again it will download a new one having a maximum of 2 files from the same feed provider.
## Kafka producer
Once the files have been processed, the Kafka producer will read the resulting list of files. The producer will:
1. Read each file.
2. When reading each file, it will look for the ```<item>``` element in the XML and will read the children nodes to form the JSON structure.
3. Produce an event that will be sent to Kafka. One event is equals to one ```<item>``` element.

For instance, having this XML feed:
```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<rss version="2.0">
    <channel>
        <title>Illinois News Bureau: Research</title>
        <link>http://illinois.edu/lb/imageList/19</link>
        <description>These are the top research articles at the University of Illinois in Urbana-Champaign.</description>
        <item>
            <title>New synthetic tumor environments make cancer research more realistic</title>
            <link>http://news.illinois.edu/news/15/0827tumor_environment_kriskilian.html</link>
            <author>Liz Ahlberg, Physical Sciences Editor</author>
            <category>Science</category>
            <comments></comments>
            <guid isPermaLink="false">http://illinois.edu/lb/article/19/94126</guid>
            <pubDate>Thu, 27 Aug 2015 08:00:00 CDT</pubDate>
            <source url="http://illinois.edu/lb/imageList/19">Illinois News Bureau: Research</source>
            <description>Tumors are notoriously difficult to study in their natural habitat – body tissues – but a new synthetic tissue environment may give cancer researchers the next-best look at tumor growth and behavior.</description>
        </item>
        <item>
            <title>Study links physical activity to greater mental flexibility in older adults</title>
            <link>http://news.illinois.edu/news/15/0824brain_aganieszkaburzynska.html</link>
            <author>Diana Yates, Life Sciences Editor</author>
            <category>Science</category>
            <comments></comments>
            <guid isPermaLink="false">http://illinois.edu/lb/article/19/93967</guid>
            <pubDate>Mon, 24 Aug 2015 08:00:00 CDT</pubDate>
            <source url="http://illinois.edu/lb/imageList/19">Illinois News Bureau: Research</source>
            <description>One day soon, doctors may be able to determine how physically active you are simply by imaging your brain. Studies have shown that physically fit people tend to have larger brain volumes and more intact white matter than their less-fit peers. Now a new study reveals that older adults who regularly engage in moderate to vigorous physical activity have more variable brain activity at rest than those who don’t. This variability is associated with better cognitive performance, the researchers say.</description>
        </item>
        <item>
            <title>Local development often at odds with regional land use plans</title>
            <link>http://news.illinois.edu/news/15/0821regionalplans_dustinallred_arnabchakraborty.html</link>
            <author>Jodi Heckel, Arts and Humanities Editor</author>
            <category>Social Sciences</category>
            <comments></comments>
            <guid isPermaLink="false">http://illinois.edu/lb/article/19/93956</guid>
            <pubDate>Fri, 21 Aug 2015 08:00:00 CDT</pubDate>
            <source url="http://illinois.edu/lb/imageList/19">Illinois News Bureau: Research</source>
            <description>A land use plan adopted for the Sacramento, California, region aimed to get local governments to plan together for development in a way that discouraged sprawl.</description>
        </item>
    </channel>
</rss>
```
Will produce 3 different events in Kafka with the following contents

```{"url": "http://news.illinois.edu/news/15/0827tumor_environment_kriskilian.html", "author": "Liz Ahlberg, Physical Sciences Editor", "description": "Tumors are notoriously difficult to study in their natural habitat \u2013 body tissues \u2013 but a new synthetic tissue environment may give cancer researchers the next-best look at tumor growth and behavior.", "title": "New synthetic tumor environments make cancer research more realistic"}```

```{"url": "http://news.illinois.edu/news/15/0824brain_aganieszkaburzynska.html", "author": "Diana Yates, Life Sciences Editor", "description": "One day soon, doctors may be able to determine how physically active you are simply by imaging your brain. Studies have shown that physically fit people tend to have larger brain volumes and more intact white matter than their less-fit peers. Now a new study reveals that older adults who regularly engage in moderate to vigorous physical activity have more variable brain activity at rest than those who don\u2019t. This variability is associated with better cognitive performance, the researchers say.", "title": "Study links physical activity to greater mental flexibility in older adults"}```

```{"url": "http://news.illinois.edu/news/15/0821regionalplans_dustinallred_arnabchakraborty.html", "author": "Jodi Heckel, Arts and Humanities Editor", "description": "A land use plan adopted for the Sacramento, California, region aimed to get local governments to plan together for development in a way that discouraged sprawl.", "title": "Local development often at odds with regional land use plans"}```

The Kafka configuration is also in this file. Make sure you point to the correct host, port and topic. See this line
[https://github.com/sosahvictor/feed-parser-kafka/blob/master/feed-parser-kafka/kafka_producer.py#L7](https://github.com/sosahvictor/feed-parser-kafka/blob/master/feed-parser-kafka/kafka_producer.py#L7)
### Important
In this file, there's also a XML parser that reads the XML files and forms the JSON structure. Currently, this parser accounts for a small set of XML namespaces, if for some reason, the feed file has a different namespace or element name than those specified in this file, the producer will fail. A great improvement would be to have this parsing in a more intelligent way. See this line.
[https://github.com/sosahvictor/feed-parser-kafka/blob/master/feed-parser-kafka/kafka_producer.py#L10](https://github.com/sosahvictor/feed-parser-kafka/blob/master/feed-parser-kafka/kafka_producer.py#L10)

# Development and testing
All python files were created locally. However, I used a docker instance to run Kafka. You can find one here
[https://hub.docker.com/r/spotify/kafka](https://hub.docker.com/r/spotify/kafka)

To install it run this command

```docker pull spotify/kafka```

Once the image is downloaded, run this command to launch the instance:

```docker run -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST=localhost --env ADVERTISED_PORT=9092 spotify/kafka```

To test the stream pipeline, you can use the consumer built-in in Kafka. For this, you will need to run a command line inside the instance. To know the instance ID run this command, you will use this ID in the next commands:

```docker ps```

Copy the instance ID from your Kafka image and then run the following

```docker exec -it <instance ID> /bin/bash```

Once in the CLI of the Kafka instance, run this command:

```/opt/kafka-<version>/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic rss --from-beginning```

Make sure you change ```kafka-<version>``` to the appropriate folder name.
This will start a process that will receive all events from the very beginning.
# Authors

* **Francisco Vargas (fav3@illinois.edu)**
* **Hari Manan (nfnh2@illinois.edu)**
* **Victor Sosa (victors3@illinois.edu)**
