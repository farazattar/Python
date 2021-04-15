import json
ip_api='{ "query": "24.48.0.1", "status": "success", "country": "Canada", "countryCode": "CA", "region": "QC", "regionName": "Quebec", "city": "Montreal", "zip": "H1K", "lat": 45.6085, "lon": -73.5493, "timezone": "America/Toronto", "isp": "Le Groupe Videotron Ltee", "org": "Videotron Ltee", "as": "AS5769 Videotron Telecom Ltee" }'
try:
    ip_api_dict=json.loads(ip_api)
except ValueError as error:
    print('This is an invalid json structure: %s' % error)
print(ip_api_dict)
print(ip_api_dict['query'])
print(ip_api_dict['region'])    
