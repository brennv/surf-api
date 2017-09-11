from forecast.config import swagger_config, template, debug, threaded
from forecast.endpoints import (Health, Point)
# , PointSwell, PointSwellDirection,
#                                 PointSwellHeight, PointSwellPeriod, PointWave,
#                                 PointWind, PointWindDirection, PointWindSpeed)
from flask import Flask, jsonify, redirect
from flask_restful import Api, Resource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app, template=template, config=swagger_config)

api.add_resource(Health, '/api/health')

api.add_resource(Point, '/api/point/<string:lat>/<string:lon>')

''' in-progress
api.add_resource(PointSwell, '/api/point/<string:lat>/<string:lon>/swell')
api.add_resource(PointSwellDirection, '/api/point/<string:lat>/<string:lon>/swell/direction')
api.add_resource(PointSwellHeight, '/api/point/<string:lat>/<string:lon>/swell/height')
api.add_resource(PointSwellPeriod, '/api/point/<string:lat>/<string:lon>/swell/period')
api.add_resource(PointWave, '/api/point/<string:lat>/<string:lon>/wave')
api.add_resource(PointWind, '/api/point/<string:lat>/<string:lon>/wind')
api.add_resource(PointWindDirection, '/api/point/<string:lat>/<string:lon>/wind/direction')
api.add_resource(PointWindSpeed, '/api/point/<string:lat>/<string:lon>/wind/speed')
'''

@app.route('/')
def index():
    return redirect('/api/spec/')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"message": "Not found"}), 404


if __name__ == '__main__':
    app.run(debug=debug, threaded=False)
