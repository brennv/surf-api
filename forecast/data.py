import requests
import xmltodict
import pandas as pd


def get_response(lat, lon):
    # latlon = '37.583,-122.952'
    # lat, lon = latlon.split(',')  # TODO decimal fmting
    url = 'http://marine.weather.gov/MapClick.php?FcstType=digitalDWML'
    url +=  '&lat=' + str(lat) + '&lon=' + str(lon)
    response = requests.get(url)
    return response

def get_data(response):
    return xmltodict.parse(response.text)

def orient_records(data, values, label):
    times = get_times(data)
    norm_len = len(values)
    times = times[:norm_len]
    return [{'time': t, label: v} for t, v in dict(zip(times, values)).items()]

def get_metadata(data):
    update = data['dwml']['head']['product']['creation-date']['#text']
    source = data['dwml']['head']['source']['credit']
    lat = data['dwml']['data']['location']['point']['@latitude']
    lon = data['dwml']['data']['location']['point']['@longitude']
    # timezone = data['dwml']['data']['time-layout']['@time-coordinate']
    area = data['dwml']['data']['location']['area-description']
    metadata = {'area': area, 'latitude': lat, 'longitude': lon, 'source': source, 'update': update}
    return metadata

def get_times(data):
    return data['dwml']['data']['time-layout']['start-valid-time']

def get_wind_direction(data, type='records'):
    values = data['dwml']['data']['parameters']['direction']['value']
    if type == 'list':
        return values
    else:
        result = get_metadata(data)
        result['forecast'] = orient_records(data, values, 'wind_direction')
        return result

def get_wind_speed(data, type='records'):
    values = data['dwml']['data']['parameters']['wind-speed'][0]['value']
    if type == 'list':
        return values
    else:
        result = get_metadata(data)
        result['forecast'] = orient_records(data, values, 'wind_speed')
        return result

def get_wave(data, type='records'):
    waves = data['dwml']['data']['parameters']['water-state']['waves']
    cut = len(waves) // 2
    values = [w['value'] for w in waves[:cut] if isinstance(w['value'], str)]
    # wave2_heights = [w['value'] for w in waves[cut:] if isinstance(w['value'], str)]
    if type == 'list':
        return values
    else:
        result = get_metadata(data)
        result['forecast'] = orient_records(data, values, 'wave_height')
        return result

def get_swell(data, include=['direction', 'height', 'period'], type='records'):
    swell = data['dwml']['data']['parameters']['water-state']['swell']
    times = get_times(data)
    swell_directions, swell_heights, swell_periods = [], [], []
    # records = []
    for i, s in enumerate(swell):
        if not isinstance(s['value'], str):
            break
        try:
            # records[i] = {'time': times[i]}
            if 'direction' in include:
                swell_dir = s['direction']
                swell_directions.append(swell_dir)
                # records[i]['swell_direction'] = swell_dir
            if 'height' in include:
                swell_ht = s['value']
                swell_heights.append(swell_ht)
                # records[i]['swell_height'] = swell_ht
            if 'period' in include:
                swell_pd = s['@period']
                swell_periods.append(swell_pd)
                # records[i]['swell_period'] = swell_pd
        except KeyError:
            # records[i]['swell_period'] = ''  # TODO
            pass
    lists = {'swell_direction': swell_directions,
             'swell_height': swell_heights,
             'swell_period': swell_periods}
    if type == 'list':
        return lists
    else:
        lists['time'] = times
        norm_len = len(lists['swell_height'])
        # print('normalized length', norm_len)
        df = pd.DataFrame()
        for k, v in lists.items():
            # print(k, v)
            df[k] = v[:norm_len] + [''] * (norm_len - len(v))
        records = df.to_dict(orient='records')
        result = get_metadata(data)
        result['forecast'] = records
        return result


def get_forecast(data):
    forecast = get_swell(data, type='list')
    forecast['time'] = get_times(data)
    forecast['wind_direction'] = get_wind_direction(data, type='list')
    forecast['wind_speed'] = get_wind_speed(data, type='list')
    forecast['wave_height'] = get_wave(data, type='list')
    # 'wave2_height': wave2_heights,
    # data['source'] = get_metadata(data)
    norm_len = len(forecast['wave_height'])
    # print('normalized length', norm_len)
    df = pd.DataFrame()
    for k, v in forecast.items():
        # print(k, v)
        df[k] = v[:norm_len] + [''] * (norm_len - len(v))
    records = df.to_dict(orient='records')
    result = get_metadata(data)
    result['forecast'] = records
    return result
