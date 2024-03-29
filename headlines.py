import feedparser
from flask import Flask
from flask import render_template
from flask import request
import pyowm


RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'jw': 'https://www.jw.org/en/news/rss/FullNewsRSS/feed.xml',
             'bloomberg': 'https://www.bloomberg.com/professional/feed/'}

list_cities = {'Dublin': '?city=dublin,ie',
                'Lome': '?city=lome,tg',
                'Paris': '?city=paris,fr',
                'Taipei': '?city=taipei,tw',
                'Bordeaux': '?city=bordeaux'}

app = Flask(__name__)


@app.route("/")
@app.route("/", methods=['GET', 'POST'])
@app.route("/<publication>")
def get_news(publication="bbc", city=None):
    feed = feedparser.parse(RSS_FEEDS[publication])
    place = request.args.get("city")
    if place is None:
        weather = owm_weather("dublin,ie")
    else:
        place = request.args.get("city")
        weather = owm_weather(place)
    return render_template("home.html", articles=feed['entries'], publication=publication, weather=weather, cities=list_cities)

def owm_weather(place):
    owm = pyowm.OWM('00cccd274676fd2894b078e918a328bb')
    observation = owm.weather_at_place(place)
    w = observation.get_weather()
    l = observation.get_location()
    weather = {"status": w.get_detailed_status(),
                "temp_avg": w.get_temperature('celsius')['temp'],
                "temp_min": w.get_temperature('celsius')['temp_min'],
                "temp_max": w.get_temperature('celsius')['temp_max'],
                "wind_speed": w.get_wind()['speed'],
                "wind_dir": w.get_wind()['deg'],
                "humidity": w.get_humidity(),
                "cloud": w.get_clouds(),
                "rain": w.get_rain(),
                "snow": w.get_snow(),
                "city": l.get_name()
                }
    return weather

@app.route('/useragent')
def useragent():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Your browser is: %s</h1>' % user_agent


if __name__ == "__main__":
    app.run(port=5000, debug=True)
