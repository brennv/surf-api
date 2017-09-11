import requests
import xmltodict
import pandas as pd

def get_data(lat, lon):
    # latlon = '37.583,-122.952'
    # lat, lon = latlon.split(',')  # TODO decimal fmting
    url = 'http://marine.weather.gov/MapClick.php?FcstType=digitalDWML'
    url +=  '&lat=' + str(lat) + '&lon=' + str(lon)
    response = requests.get(url).text
    return xmltodict.parse(response)

def get_metadata(response):
    update = response['dwml']['head']['product']['creation-date']['#text']
    source = response['dwml']['head']['source']['credit']
    lat = response['dwml']['data']['location']['point']['@latitude']
    lon = response['dwml']['data']['location']['point']['@longitude']
    # timezone = response['dwml']['data']['time-layout']['@time-coordinate']
    area = response['dwml']['data']['location']['area-description']
    metadata = {'area': area, 'latitude': lat, 'longitude': lon, 'source': source, 'update': update}
    return metadata

def get_times(response):
    return response['dwml']['data']['time-layout']['start-valid-time']

def get_wind_direction(response):
    return response['dwml']['data']['parameters']['direction']['value']

def get_wind_speed(response):
    return response['dwml']['data']['parameters']['wind-speed'][0]['value']

def get_wave(response):
    waves = response['dwml']['data']['parameters']['water-state']['waves']
    cut = len(waves) // 2
    wave1_heights = [w['value'] for w in waves[:cut] if isinstance(w['value'], str)]
    # wave2_heights = [w['value'] for w in waves[cut:] if isinstance(w['value'], str)]
    return wave1_heights

def get_swell(response, include=['direction', 'height', 'period']):
    swell = response['dwml']['data']['parameters']['water-state']['swell']
    swell_directions, swell_heights, swell_periods = [], [], []
    for s in swell:
        if not isinstance(s['value'], str):
            break
        try:
            if 'direction' in include:
                swell_directions.append(s['direction'])
            if 'height' in include:
                swell_heights.append(s['value'])
            if 'period' in include:
                swell_periods.append(s['@period'])
        except KeyError:
            pass
    return {'swell_direction': swell_directions,
            'swell_height': swell_heights,
            'swell_period': swell_periods}

def get_forecast(response):
    forecast = get_swell(response)
    forecast['time'] = get_times(response)
    forecast['wind_direction'] = get_wind_direction(response)
    forecast['wind_speed'] = get_wind_speed(response)
    forecast['wave_height'] = get_wave(response)
    # 'wave2_height': wave2_heights,
    # data['source'] = get_metadata(response)
    norm_len = len(forecast['wave_height'])
    df = pd.DataFrame()
    for k, v in data.items():
        df[k] = v[:norm_len] + [''] * (norm_len - len(v))
    records = df.to_dict(orient='records')
    data = get_metadata(response)
    data['forecast'] = records
    return data

def orient_records(response, values, label):
    times = get_times(response)
    norm_len = len(values)
    times = times[:norm_len]
    return [{'time': t, label: v} for t, v in dict(zip(times, values)).items()]


# df_temp = pd.DataFrame()
# df_temp['time'] = df['time']
# df_temp['swell_height'] = df['swell_height']
