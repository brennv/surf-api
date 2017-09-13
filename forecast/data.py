import requests
import xmltodict
import pandas as pd


def get_response(lat, lon):
    # TODO clean inputs, trim floats
    url = 'http://marine.weather.gov/MapClick.php?FcstType=digitalDWML'
    url +=  '&lat=' + str(lat) + '&lon=' + str(lon)
    print(url)
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        # This will only happen after a very long time
        # TODO timeout this function and raise error
        pass
    return response


def get_data(response):
    return xmltodict.parse(response.text)


def include_time(data, values, label):
    times = get_times(data)
    times = times[:len(values)]
    return [{'time': t, label: v} for t, v in dict(zip(times, values)).items()]


def normalize_records(data, norm):
    """ Reshape a dict of lists as a list of dicts. If list lengths are
        inconsistent, normalize lists with a non-value. """
    norm_len = len(data[norm])
    df = pd.DataFrame()
    for k, v in data.items():
        df[k] = v[:norm_len] + [''] * (norm_len - len(v))
    records = df.to_dict(orient='records')
    return records


def get_metadata(data):
    update = data['dwml']['head']['product']['creation-date']['#text']
    source = data['dwml']['head']['source']['credit']
    lat = data['dwml']['data']['location']['point']['@latitude']
    lon = data['dwml']['data']['location']['point']['@longitude']
    # timezone = data['dwml']['data']['time-layout']['@time-coordinate']
    area = data['dwml']['data']['location']['area-description']
    metadata = {'area': area, 'latitude': lat, 'longitude': lon,
                'source': source, 'update': update}
    return metadata


def get_times(data):
    return data['dwml']['data']['time-layout']['start-valid-time']


def get_wind_direction(data, orient='records'):
    values = data['dwml']['data']['parameters']['direction']['value']
    if orient == 'list':
        return values
    else:
        result = get_metadata(data)
        result['forecast'] = include_time(data, values, 'wind_direction')
        return result


def get_wind_speed(data, orient='records'):
    values = data['dwml']['data']['parameters']['wind-speed'][0]['value']
    if orient == 'list':
        return values
    else:
        result = get_metadata(data)
        result['forecast'] = include_time(data, values, 'wind_speed')
        return result


def get_wave(data, orient='records'):
    waves = data['dwml']['data']['parameters']['water-state']['waves']
    cut = len(waves) // 2
    values = [w['value'] for w in waves[:cut] if isinstance(w['value'], str)]
    # wave2_heights = [w['value'] for w in waves[cut:] if isinstance(w['value'], str)]
    if orient == 'list':
        return values
    else:
        result = get_metadata(data)
        result['forecast'] = include_time(data, values, 'wave_height')
        return result


def get_swell(data, orient='records'):
    swell = data['dwml']['data']['parameters']['water-state']['swell']
    swell_directions, swell_heights, swell_periods = [], [], []
    for s in swell:
        if not isinstance(s['value'], str):
            # Stop when we've reached the end of heights
            break
        try:
            swell_dir = s['direction']
            swell_directions.append(swell_dir)
            swell_ht = s['value']
            swell_heights.append(swell_ht)
            swell_pd = s['@period']
            swell_periods.append(swell_pd)
        except KeyError:
            # Period is not forecasted as far into the future as height and dir
            pass
    forecast = {'time': get_times(data),
                'swell_direction': swell_directions,
                'swell_height': swell_heights,
                'swell_period': swell_periods}
    if orient == 'list':
        return forecast
    else:
        result = get_metadata(data)
        result['forecast'] = normalize_records(forecast, norm='swell_height')
        return result


def get_forecast(data):
    forecast = get_swell(data, orient='list')
    forecast['wind_direction'] = get_wind_direction(data, orient='list')
    forecast['wind_speed'] = get_wind_speed(data, orient='list')
    forecast['wave_height'] = get_wave(data, orient='list')
    # TODO 'wave2_height': wave2_heights,
    result = get_metadata(data)
    result['forecast'] = normalize_records(forecast, norm='wave_height')
    return result
