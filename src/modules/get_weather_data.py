import pandas as pd
import requests 
import json
from keys import API_KEYS

api_keys = API_KEYS()
api_key = api_keys.api_key

top_airport_codes = pd.read_csv('../../data/top-airports.csv')
top_airport_codes = list(top_airport_codes['airport'][:20].to_numpy())
airport_latlong = pd.read_csv('../../data/airport-codes_csv.csv')

start_date = ['2018-01-01', '2018-02-01', '2018-03-01', '2018-04-01', '2018-05-01', '2018-06-01',
              '2018-07-01', '2018-08-01', '2018-09-01', '2018-10-01', '2018-11-01', '2018-12-01',
              '2019-01-01', '2019-02-01', '2019-03-01', '2019-04-01', '2019-05-01', '2019-06-01',
              '2019-07-01', '2019-08-01', '2019-09-01', '2019-10-01', '2019-11-01', '2019-12-01']
end_date = ['2018-01-31', '2018-02-28', '2018-03-31', '2018-04-30', '2018-05-31', '2018-06-30',
            '2018-07-31', '2018-08-31', '2018-09-30', '2018-10-31', '2018-11-30', '2018-12-31',
            '2019-01-31', '2019-02-28', '2019-03-31', '2019-04-30', '2019-05-31', '2019-06-30',
            '2019-07-31', '2019-08-31', '2019-09-30', '2019-10-31', '2019-11-30', '2019-12-31',]

def get_latlong(airport_latlong, code):
    latitude = airport_latlong[airport_latlong['iata_code'] == code]['coordinates'].values[0].split()[0]
    longitude = airport_latlong[airport_latlong['iata_code'] == code]['coordinates'].values[0].split()[1]
    return latitude,longitude

def get_weather_data(code, start_date, end_date):
    base_url = 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx'
    params = {'q': code, 'date': start_date, 
              'enddate': end_date, 'tp': 24, 'format': 'json', 'key': api_key}

    response = requests.get(base_url, params=params)
    status_code = response.status_code

    if status_code != 200:
        print(f'Error: {status_code}')
        return
    else:
        return response.json()

def store_weather_data(data, code, num):
    with open(f'../../data/weather-data/{code}_{num}.json', 'w') as f:
        json.dump(data, f)

def get_all_weather(airport_codes, start_date, end_date):
    for code in airport_codes:
        for i in range(len(start_date)):
            weather_data = get_weather_data(code, start_date[i], end_date[i])
            store_weather_data(weather_data, code, i)

def parse_weather_json(airport_codes):

    column_names = ['iata_code', 'date', 'min_temp', 'max_temp', 'avg_temp', 'total_snowcm',
                'windspeed_kmhr', 'precip_mm', 'humidity', 'visibility', 'cloud_cover',
                'heat_indexC', 'wind_chillC', 'wind_gust', 'feels_like']

    weather_df = pd.DataFrame(columns=column_names, dtype=object)

    for code in airport_codes:
        for k in range(24):
            f = open(f'../../data/weather-data/{code}_{k}.json')
            data = json.load(f)
            path = data['data']['weather']
            for i in range(len(path)):
                iata_code = code
                date = path[i]['date']
                min_temp = path[i]['mintempC']
                max_temp = path[i]['maxtempC']
                avg_temp = path[i]['avgtempC']
                total_snowcm = path[i]['totalSnow_cm']
                windspeed_kmhr = path[i]['hourly'][0]['windspeedKmph']
                precip_mm = path[i]['hourly'][0]['precipMM']
                humidity = path[i]['hourly'][0]['humidity']
                visibility = path[i]['hourly'][0]['visibility']
                cloud_cover = path[i]['hourly'][0]['cloudcover']
                heat_indexC = path[i]['hourly'][0]['HeatIndexC']
                wind_chillC = path[i]['hourly'][0]['WindChillC']
                wind_gust = path[i]['hourly'][0]['WindGustKmph']
                feels_like = path[i]['hourly'][0]['FeelsLikeC']

                weather_list = [iata_code, date, min_temp, max_temp, avg_temp, total_snowcm,
                            windspeed_kmhr, precip_mm, humidity, visibility, cloud_cover,
                            heat_indexC, wind_chillC, wind_gust, feels_like]
                weather_series = pd.Series(weather_list, index=weather_df.columns)

                weather_df = weather_df.append(weather_series, ignore_index=True)