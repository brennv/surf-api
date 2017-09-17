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


def parse_data(response):
    return xmltodict.parse(response.text)


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


def get_times(data, pretty=False):
    times = data['dwml']['data']['time-layout']['start-valid-time']
    if pretty:
        times = [t[5:-9].replace('T', ' ') for t in times]
    return times


def add_metadata(data, values, label):
    """ Wrap a list values with metadata and inlude value times. """
    result = get_metadata(data)
    times = get_times(data)
    times = times[:len(values)]
    result['forecast'] = [{'time': t, label: v} for t, v in
                          dict(zip(times, values)).items()]
    return result


def normalize_records(data, norm):
    """ Reshape a dict of lists as a list of dicts. If list lengths are
        inconsistent, normalize lists with a non-value. """
    norm_len = len(data[norm])
    df = pd.DataFrame()
    for k, v in data.items():
        df[k] = v[:norm_len] + [''] * (norm_len - len(v))
    records = df.to_dict(orient='records')
    return records


def get_wind_direction(data, meta=True):
    result = data['dwml']['data']['parameters']['direction']['value']
    if meta:
        result = add_metadata(data, result, 'wind_direction')
    return result


def get_wind_speed(data, meta=True):
    result = data['dwml']['data']['parameters']['wind-speed'][0]['value']
    if meta:
        result = add_metadata(data, result, 'wind_speed')
    return result


def get_wave(data, meta=True):
    waves = data['dwml']['data']['parameters']['water-state']['waves']
    cut = len(waves) // 2
    result = [w['value'] for w in waves[:cut] if isinstance(w['value'], str)]
    # wave2_heights = [w['value'] for w in waves[cut:] if isinstance(w['value'], str)]
    if meta:
        result = add_metadata(data, result, 'wave_height')
    return result


def get_swell(data, meta=True):
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
    if meta:
        forecast, results = get_metadata(data), forecast
        forecast['forecast'] = normalize_records(results, norm='swell_height')
    return forecast


def get_forecast(data):
    forecast = get_metadata(data)
    results = get_swell(data, meta=False)
    results['wind_direction'] = get_wind_direction(data, meta=False)
    results['wind_speed'] = get_wind_speed(data, meta=False)
    results['wave_height'] = get_wave(data, meta=False)
    forecast['forecast'] = normalize_records(results, norm='wave_height')
    return forecast
