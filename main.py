import feedparser

feeds = [
    "https://www.manutd.com/en/rss/news",
    "https://feeds.bbci.co.uk/sport/football/rss.xml"
]

print("Manchester United News")

for feed in feeds:
    d = feedparser.parse(feed)

    for entry in d.entries[:5]:
        title = entry.title

        if "united" in title.lower() or "manchester" in title.lower():
            print(title)
