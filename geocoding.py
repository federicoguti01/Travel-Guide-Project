import requests
from config import GEO_KEY, CLIENT_ID, CLIENT_SECRET


def getLufthansaAuth():
    AUTH_URL = 'https://api.lufthansa.com/v1/oauth/token'
    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    
    auth_response_data = auth_response.json()
    
    access_token = auth_response_data['access_token']
    
    headers = {
        "Accept": "application/json",
        'Authorization': f'Bearer {access_token}'
    }
    
    return headers


def getGeocode(location):
    GEO_URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={GEO_KEY}'
    decoder = requests.get(GEO_URL)
    dJSON = decoder.json()
    
#     address = dJSON['results'][0]['address_components']
#     country = ''
#     for component in address:
#         if 'country' in component['types']:
#             countryCode = component['short_name']


    geoloc = dJSON['results'][0]['geometry']['location']
    return [geoloc['lat'], geoloc['lng']]


def getManyIATA(coords):
    IATA_URL = f'https://api.lufthansa.com/v1/references/airports/nearest/{coords[0]},{coords[1]}'
    decoder = requests.get(IATA_URL, headers=getLufthansaAuth())
    dJSON = decoder.json()
    
    airports = dJSON['NearestAirportResource']['Airports']['Airport']
    portList = []
    for airport in airports:
        portList.append(airport['AirportCode'])
        
    return portList
  
  
def getIATA(coords):
    IATA_URL = f'http://iatageo.com/getCode/{coords[0]}/{coords[1]}'
    decoder = requests.get(IATA_URL)
    dJSON = decoder.json()
    
    return dJSON['IATA']


def main():
    location = input('Enter a location: ')
    coords = getGeocode(location)
    print(getManyIATA(coords))

if __name__ == "__main__":
    main()
