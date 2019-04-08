from textblob import TextBlob
from rake_nltk import Rake
import time
import json
import re

# Sample RSS Feed for testing purposes
rssData = '''
{
  "title": "3 Questions: Why are student-athletes amateurs?",
  "author": "Peter Dizikes | MIT News Office",
  "description": "MIT Professor Jennifer Light digs into the history of the idea that students aren\u2019t part of the labor force.",
  "url": "http://news.mit.edu/2019/jennifer-light-student-athletes-0325"
}
'''

def extractKeyword(text):
  # Extract keywords from text and return maximum 3
  r = Rake()
  r.extract_keywords_from_text(cleanText(text))
  resultKeyword = r.get_ranked_phrases()
  if(len(resultKeyword)>2):
        return resultKeyword[:3]
  else:
        return resultKeyword[:2]

def extractSentiment(text):
  # Get polarity values and return sentiment type
  analysis = TextBlob(cleanText(text))
  if analysis.sentiment.polarity > 0:
    return 'positive'
  elif analysis.sentiment.polarity == 0:
    return 'neutral'
  else:
    return 'negative'

def cleanText(text):
  # Apply RegEx substitution to clean the description from weird characters
  return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+) ", " ", text).split())

def parseJSON(data):
  # Load JSON RSS Feed input
  data = json.loads(data)   

  # Add timestamps as key, sentiments, and keywords to the digested RSS Feed
  data['key'] = time.time();

  # Only if description exists we should apply the NLP analysis
  if data["description"]:
    data['sentiment'] = extractSentiment(data["description"])
    data['keyword'] = extractKeyword(data["description"])
  else:
    data['sentiment'] = ""
    data['keyword'] = ""

  # Re-construct JSON and return output
  parsedFeed = json.dumps(data, indent = 2)
  return parsedFeed