from requests import request
import xmltodict
import vlc
from pprint import pprint

def play_weather_audio_from_yle():
    # https://feeds.yle.fi/areena/v1/series/1-1257538.rss?lang=fi&downloadable=true
    feed = request(url="https://feeds.yle.fi/areena/v1/series/1-1257538.rss?lang=fi&downloadable=true", method="get")
    feed_dict = xmltodict.parse(feed.text)

    weather_link = feed_dict["rss"]["channel"]["item"][0]["link"]
    player = vlc.MediaPlayer(weather_link)
    player.play()

def play_jazz_radio():
    vlc.MediaPlayer("http://broadcast.infomaniak.ch/jazzradio-high.mp3.m3u").play()

def play_rock_radio():
    vlc.MediaPlayer("http://webradio.antennevorarlberg.at/classicrock.m3u").play()
