# surf-api

RESTful json-formatted NOAA Marine Weather forecasts and surf spot metadata

See: [surfcast.vonapp.co](http://surfcast.vonapp.co)

## Endpoints

### point: forecasts by latitude, longitude

GET **/api/point/{lat,lon}** Forecast for point

#### Example point forecast response

```
{
  "area": "28NM WSW San Francisco CA",
  "latitude": "37.59",
  "longitude": "-122.97",
  "source": "http://www.wrh.noaa.gov/mtr",
  "update": "2017-09-10T14:22:36-07:00",
  "forecast": [
    {
      "swell_direction": "300",
      "swell_height": "4",
      "swell_period": "14",
      "time": "2017-09-10T18:00:00-07:00",
      "wind_direction": "310",
      "wind_speed": "10",
      "wave_height": "4"
    },
    {
      "swell_direction": "300",
      "swell_height": "4",
      "swell_period": "14",
      "time": "2017-09-10T19:00:00-07:00",
      "wind_direction": "310",
      "wind_speed": "10",
      "wave_height": "4"
    },
    ..
    {
      "swell_direction": "320",
      "swell_height": "6",
      "swell_period": "",
      "time": "2017-09-16T22:00:00-07:00",
      "wind_direction": "300",
      "wind_speed": "15",
      "wave_height": "6"
    }
  ]
}
```

### status

GET **/api/health** API health check

## in-progress

### point

GET **/api/point/{lat,lon}/swell** Swell direction, height, period

GET **/api/point/{lat,lon}/swell/direction** Swell direction

GET **/api/point/{lat,lon}/swell/height** Swell height

GET **/api/point/{lat,lon}/swell/period** Swell period

GET **/api/point/{lat,lon}/wave** Wave height

GET **/api/point/{lat,lon}/wind** Wind direction, speed

GET **/api/point/{lat,lon}/wind/direction** Wind direction

GET **/api/point/{lat,lon}/wind/speed** Wind speed

### spots: list surf spots

GET **/api/spots** List of surf spots

GET **/api/spots/near/{lat,lon,radius}** Surf spots by location

### spot: forecasts by spot id

GET **/api/spot/{id}** Forecast for surf pots

GET **/api/spot/{id}/swell** Swell direction, height, period

GET **/api/spot/{id}/swell/direction** Swell direction

GET **/api/spot/{id}/swell/height** Swell height

GET **/api/spot/{id}/swell/period** Swell period

GET **/api/spot/{id}/wave** Wave height

GET **/api/spot/{id}/wind** Wind direction, speed

GET **/api/spot/{id}/wind/direction** Wind direction

GET **/api/spot/{id}/wind/speed** Wind speed
