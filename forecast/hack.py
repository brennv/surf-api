# hacky code generator

# /api/point/{lat,lon}; Forecast for point
endpoints = """/api/point/{lat,lon}/swell; Swell direction, height, period
/api/point/{lat,lon}/swell/direction; Swell direction
/api/point/{lat,lon}/swell/height; Swell height
/api/point/{lat,lon}/swell/period; Swell period
/api/point/{lat,lon}/wave; Wave height
/api/point/{lat,lon}/wind; Wind direction, speed
/api/point/{lat,lon}/wind/direction; Wind direction
/api/point/{lat,lon}/wind/speed; Wind speed"""

"""
/api/spots; List of surf spots
/api/spots/near/{lat,lon,radius}; Surf spots by location
/api/spot/{id}; Forecast for surf pots
/api/spot/{id}/swell; Swell direction, height, period
/api/spot/{id}/swell/direction; Swell direction
/api/spot/{id}/swell/height; Swell height
/api/spot/{id}/swell/period; Swell period
/api/spot/{id}/wave; Wave height
/api/spot/{id}/wind; Wind direction, speed
/api/spot/{id}/wind/direction; Wind direction
/api/spot/{id}/wind/speed; Wind speed
"""

classes, methods, addresses = [], [], []
for e in endpoints.split('\n'):
    address, description = e.split('; ')
    addresses.append(address)
    pre, name = address.split('}/')
    tag = pre.split('/')[2]
    names = name.split('/')
    name = [n.title() for n in names]
    name = tag.title() + ''.join(name)
    classes.append(name)
    get = 'get_' + '_'.join(names)
    methods.append(get)
    default = '37.583,-122.952'
    param = pre.split('{')[-1].replace(',', '')
    print(f'''
class {name}(Resource):
    def get(self, {param}):
        """
        {description}
        ---
        tags:
          - {tag}
        parameters:
          - name: {param}
            in: path
            type: string
            required: true
            default: {default}
        responses:
         200:
           description: {description}
        """
        return {get}({param}), 200''', '\n')

for c, a in dict(zip(classes, addresses)).items():
    a = a.replace('{', '<string:')
    a = a.replace('}', '>')
    a = a.replace(',', '')
    print(f"api.add_resource({c}, '{a}')")

print(', '. join(classes))
print(', '. join(methods))
