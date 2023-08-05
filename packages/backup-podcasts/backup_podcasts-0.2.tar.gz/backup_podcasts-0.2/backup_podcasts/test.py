import feedparser

rss = feedparser.parse("http://podcast.open.ac.uk/feeds/thoughtexperiments-01/rss2.xml")
print(rss.entries[0]["link"])