import feedparser
from flask import Flask
from flask import render_template
from flask import request

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'jw': 'https://www.jw.org/en/news/rss/FullNewsRSS/feed.xml',
             'bloomberg': 'https://www.bloomberg.com/professional/feed/'}

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def get_news():
    #query = request.arg.get("publication")
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return render_template("home.html", articles=feed['entries'], publication=publication)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
