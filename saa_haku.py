from datetime import date, datetime, timedelta
from time import sleep
from requests import request
from heratyskello_kirjasto import get_weather_from_ilmatieteenlaitos
from player import play_weather_audio_from_yle
from player import play_jazz_radio
from player import play_rock_radio


def main(hour, minute):

    wake_up_time = datetime.now().replace(hour=hour, minute=minute, second=0)
    weather = get_weather_from_ilmatieteenlaitos(wake_up_time)
    extra_time_minutes = 0
    play_weather = False

    # Varaa aikaa lumitöille
    if weather.rain_amount_night > 10:  # [mm]
        extra_time_minutes += 30
        play_weather = True

    # Muista laittaa auto lämmitykseen
    if weather.low_temp_morning < 3:
        extra_time_minutes += 10
        play_weather = True

    # Varmista, ettei putket jäädy
    if weather.low_temp_day < -20:
        extra_time_minutes += 10
        play_weather = True

    if datetime.now() > wake_up_time - timedelta(minutes=extra_time_minutes):  # TODO: check units
        if play_weather:
            play_weather_audio_from_yle()
            play_rock_radio()
        else:
            play_jazz_radio()
    else:
        sleep(60)  # lets wait 60 seconds before doing this all over again

main(1, 57)
