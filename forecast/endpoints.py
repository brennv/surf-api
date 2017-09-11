from .data import (get_data, get_forecast, get_swell, get_wave, get_wind_direction,
                   get_wind_speed)
# get_swell_direction, get_swell_height, get_swell_period, get_wind,
from flask_restful import Resource


class Health(Resource):
    def get(self):
        """
        API health check
        ---
        tags:
          - status
        responses:
         200:
           description: Status check
        """
        return {'status': 'ok'}, 200


class Point(Resource):
    def get(self, lat, lon):
        """
        Point forecast
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Point forecast
        """
        response = get_data(lat, lon)
        return get_forecast(response), 200

'''
class PointSwell(Resource):
    def get(self, lat, lon):
        """
        Swell direction, height, period
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Swell direction, height, period
        """
        return get_swell(lat, lon), 200


class PointSwellDirection(Resource):
    def get(self, lat, lon):
        """
        Swell direction
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Swell direction
        """
        return get_swell_direction(lat, lon), 200


class PointSwellHeight(Resource):
    def get(self, lat, lon):
        """
        Swell height
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Swell height
        """
        return get_swell_height(lat, lon), 200


class PointSwellPeriod(Resource):
    def get(self, lat, lon):
        """
        Swell period
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Swell period
        """
        return get_swell_period(lat, lon), 200


class PointWave(Resource):
    def get(self, lat, lon):
        """
        Wave height
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Wave height
        """
        return get_wave(lat, lon), 200


class PointWind(Resource):
    def get(self, lat, lon):
        """
        Wind direction, speed
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Wind direction, speed
        """
        return get_wind(lat, lon), 200


class PointWindDirection(Resource):
    def get(self, lat, lon):
        """
        Wind direction
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Wind direction
        """
        return get_wind_direction(lat, lon), 200


class PointWindSpeed(Resource):
    def get(self, lat, lon):
        """
        Wind speed
        ---
        tags:
          - point
        parameters:
          - name: lat
            in: path
            type: string
            required: true
            default: 37.583
          - name: lon
            in: path
            type: string
            required: true
            default: -122.952
        responses:
         200:
           description: Wind speed
        """
        return get_wind_speed(lat, lon), 200
'''
