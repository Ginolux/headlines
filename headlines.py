import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import urllib2
import urllib

import pyowm


RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'jw': 'https://www.jw.org/en/news/rss/FullNewsRSS/feed.xml',
             'bloomberg': 'https://www.bloomberg.com/professional/feed/'}

app = Flask(__name__)

@app.route("/")
#@app.route("/", methods=['GET', 'POST'])
@app.route("/<publication>")
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = owm_weather('dublin,ie')
    return render_template("home.html", articles=feed['entries'], publication=publication, weather=weather)

def owm_weather(place):
    owm = pyowm.OWM('00cccd274676fd2894b078e918a328bb')
    observation = owm.weather_at_place(place)
    w = observation.get_weather()
    l = observation.get_location()
    weather = {"status": w.get_detailed_status(),
                "temp_avg": w.get_temperature('celsius')['temp'],
                "temp_min": w.get_temperature('celsius')['temp_min'],
                "temp_max": w.get_temperature('celsius')['temp_max'],
                "wind": w.get_wind(),
                "humidity": w.get_humidity(),
                "cloud": w.get_clouds(),
                "rain": w.get_rain(),
                "snow": w.get_snow(),
                "city": l.get_name()
                }
    return weather


if __name__ == "__main__":
    app.run(port=5000, debug=True)
