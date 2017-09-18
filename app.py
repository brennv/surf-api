from forecast.config import swagger_config, template, debug, threaded
from forecast.endpoints import (Health, Point, PointSwell, PointWindDirection,
                                PointSwell, PointWindSpeed, PointWave)
from forecast.data import (get_response, parse_data, get_wave, get_times,
                           get_metadata, get_wind_speed, get_wind_direction,
                           get_swell)
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_restful import Api, Resource
from flasgger import Swagger
import uuid
import math


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
api = Api(app)
swagger = Swagger(app, template=template, config=swagger_config)

api.add_resource(Health, '/api/health')
api.add_resource(Point, '/api/point/<string:lat>/<string:lon>')
api.add_resource(PointSwell, '/api/point/<string:lat>/<string:lon>/swell')
api.add_resource(PointWindDirection, '/api/point/<string:lat>/<string:lon>/wind/direction')
api.add_resource(PointWindSpeed, '/api/point/<string:lat>/<string:lon>/wind/speed')
api.add_resource(PointWave, '/api/point/<string:lat>/<string:lon>/wave')

''' in-progress
api.add_resource(PointSwellDirection, '/api/point/<string:lat>/<string:lon>/swell/direction')
api.add_resource(PointSwellHeight, '/api/point/<string:lat>/<string:lon>/swell/height')
api.add_resource(PointSwellPeriod, '/api/point/<string:lat>/<string:lon>/swell/period')
api.add_resource(PointWind, '/api/point/<string:lat>/<string:lon>/wind')
'''


@app.route('/', methods=['GET', 'POST'])
def chart():
    coord = session.get('coord', '37.583, -122.952')
    times, borders, fills = [], [], []
    swell, meta, y_max = {}, {}, {}
    error = ''
    if request.form:
        coord = request.form['coord'] or coord
    session['coord'] = coord
    try:
        lat, lon = coord.strip().split(',')
        lat, lon = lat.strip(), lon.strip()
        response = get_response(lat, lon)
        if response.status_code == 200:
            data = parse_data(response)
            waves = get_wave(data, meta=False)
            times = get_times(data, pretty=True)[:len(waves)]
            swell = get_swell(data, meta=False)
            swell['wave_height'] = waves
            swell['wind_direction'] = get_wind_direction(data, meta=False)[:len(waves)]
            swell['wind_speed'] = get_wind_speed(data, meta=False)[:len(waves)]
            swell['swell_direction'] = swell['swell_direction'][:len(waves)]
            dir_range =[int(x) for x in swell['wind_direction'] + swell['swell_direction']]
            direction_min, direction_max = min(dir_range) - 20 , max(dir_range) + 1
            direction_min = max([int(math.ceil(direction_min / 20.0)) * 20, 0])
            direction_max = min([int(math.ceil(direction_max / 20.0)) * 20, 360])
            wave_max = max([int(x) for x in swell['wave_height']]) + 1
            wind_max = max([int(x) for x in swell['wind_speed']]) + 1
            wave_height_max = int(math.ceil(wave_max / 2.0)) * 2
            scale = {'wave_height_max': wave_height_max,
                     'wind_speed_max': int(math.ceil(wind_max / 5.0)) * 5,
                     'direction_min': direction_min,
                     'direction_max': direction_max,
                     'direction_step': (direction_max - direction_min) / 4,
                     'left_pad': 8 if wave_height_max >= 10 else 16}
            meta = get_metadata(data)
            meta['update'] = meta['update'][:-9].replace('T', ' ')
            meta['source'] = 'weather.gov/' + meta['source'].split('/')[-1]
    except Exception as e:
        print('error:', e)
        if 'not enough values to unpack' in str(e):
            error = 'Please use a comma beteen numbers.'
        elif 'mismatched tag' in str(e) or 'water-state' in str(e):
            error = 'No near-shore ocean forecast available for that coordinate.'
        else:
            error = 'No near-shore ocean forecast available.'
            # raise e
    if error:
        error += ' The expected decimal coordinate is: latitude, longitude'
    return render_template('chart.html', times=times, data=swell,
                           error=error, meta=meta, coord=coord, scale=scale)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Not found"}), 404


if __name__ == '__main__':
    app.run(debug=debug, threaded=False)
