import os

host = os.getenv('SURF_API_HOST', '127.0.0.1:5000')
scheme = [x for x in [os.getenv('SURF_API_SCHEME')] if x]

template = {
  # "host": "surf.vonapp.co",
  "host": host,
  # "schemes": ["https"],
  "schemes": scheme,
  # "schemes": ["https", "http"],
  "swagger": "2.0",
  "info": {
    "title": "Surf Forecast API",
    "description": "API endpoints for surf.vonapp.co",
    "version": "0.1.0"
  },
  "basePath": "/",
  "operationId": "get_data",
  # set tag order
  "tags": [
      {"name": "point", "description": "Forecast data by coordinate"},
      {"name": "status", "description": "Health check"},
  ]
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'spec',
            "name": 'surf',
            "route": '/api/spec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/spec/",
    'title': 'Surf Forecast API',
}

if host == '127.0.0.1:5000':
    debug = True
    threaded = False
else:
    debug = False
    threaded = True

print(' * Host:', host)
print(' * Scheme:', scheme)
print(' * Debug:', debug)
print(' * Threaded:', threaded)
