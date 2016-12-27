from requests import request
from collections import namedtuple
import xmltodict
from collections import OrderedDict
import time
import datetime


weather = namedtuple("Weather", ("rain_amount_night low_temp_morning low_temp_day"))
apikey = ""  # add me


def get_weather_from_ilmatieteenlaitos(wake_up_time):
    query = "http://data.fmi.fi/fmi-apikey/{apikey}/wfs".format(apikey=apikey)
    params = {
        "request": "getFeature",
        "storedquery_id": "fmi::forecast::hirlam::surface::point::multipointcoverage",
        "place": "helsinki"
    }
    response = request(url=query, params=params, method="get")
    xml_dict = xmltodict.parse(response.text)

    points_string = xml_dict["wfs:FeatureCollection"]["wfs:member"]["omso:GridSeriesObservation"]["om:result"]["gmlcov:MultiPointCoverage"]["gml:domainSet"]["gmlcov:SimpleMultiPoint"]["gmlcov:positions"]
    data_string = xml_dict["wfs:FeatureCollection"]["wfs:member"]["omso:GridSeriesObservation"]["om:result"]["gmlcov:MultiPointCoverage"]["gml:rangeSet"]["gml:DataBlock"]["gml:doubleOrNilReasonTupleList"]
    points = points_string.split("\n")
    data = data_string.split("\n")

    morning_temp = None
    start_time = None
    coldest = 99999

    for p, d in OrderedDict(zip(points, data)).items():
        this_time = p.strip().split()[2]
        dtm = datetime.datetime.fromtimestamp(int(this_time))
        temp = d.strip().split()[1]
        rain1 = d.strip().split()[16]
        rain2 = d.strip().split()[17]
        if dtm > wake_up_time and not morning_temp:
            morning_temp = float(temp)
            morning_time = dtm
            start_time = dtm
            rain_amount_night = float(rain2)

        if start_time:
            if start_time + datetime.timedelta(hours=18) > dtm:
                if coldest > float(temp):
                    coldest = float(temp)
                    coldest_time = dtm

        print(rain1, rain2)

    print("morning temp: ", morning_time.strftime('%Y-%m-%d %H:%M:%S'), morning_temp)
    print("coldest temp: ", coldest_time.strftime('%Y-%m-%d %H:%M:%S'), coldest)

    low_temp_morning = 0
    low_temp_day = 0
    rain_amount_night = 0
    return weather(low_temp_morning=morning_temp, low_temp_day=coldest, rain_amount_night=rain_amount_night)

if __name__ == "__main__":
    get_weather_from_ilmatieteenlaitos(datetime.datetime.today() + datetime.timedelta(hours=12))
