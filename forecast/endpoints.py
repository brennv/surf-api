from .data import (get_response, parse_data, get_forecast, get_swell, get_wave,
                   get_wind_direction, get_wind_speed)
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
        response = get_response(lat, lon)
        if response.status_code == 200:
            data = parse_data(response)
            result = get_forecast(data)
        else:
            result = {}
        return result, response.status_code


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
        response = get_response(lat, lon)
        if response.status_code == 200:
            data = parse_data(response)
            result = get_swell(data)
        else:
            result = {}
        return result, response.status_code

'''
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
        return get_swell_direction(lat, lon), response.status_code


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
        return get_swell_height(lat, lon), response.status_code


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
        return get_swell_period(lat, lon), response.status_code
'''

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
        response = get_response(lat, lon)
        if response.status_code == 200:
            data = parse_data(response)
            result = get_wave(data)
        else:
            result = {}
        return result, response.status_code

'''
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
        return get_wind(lat, lon), response.status_code
'''

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
        response = get_response(lat, lon)
        if response.status_code == 200:
            data = parse_data(response)
            result = get_wind_direction(data)
        else:
            result = {}
        return result, response.status_code


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
        response = get_response(lat, lon)
        if response.status_code == 200:
            data = parse_data(response)
            result = get_wind_speed(data)
        else:
            result = {}
        return result, response.status_code
