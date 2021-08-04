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


def reverseGeocode(lat, lng):
    GEO_URL = ('https://maps.googleapis.com/maps/api/geocode/json?'
               f'latlng={lat},{lng}&key={GEO_KEY}')
    decoder = requests.get(GEO_URL)
    dJSON = decoder.json()

    if dJSON['status'] == 'OK':

        address = dJSON['results'][0]['address_components']
        name = ''
        #         print(dJSON)
        for component in address:
            if 'country' in component['types']:
                name += component['long_name']
            elif 'street_number' in component['types']:
                name += component['long_name'] + " "
            elif 'postal_code' in component['types']:
                name += ' ' + str(component['long_name'])
            elif 'administrative_area_level_2' in component['types'] or \
                    'postal_code_suffix' in component['types']:
                pass
            else:
                name += component['short_name'] + ", "

        return name

    return None


def reverseGeoCity(lat, lng):
    GEO_URL = ('https://maps.googleapis.com/maps/api/geocode/json?'
               f'latlng={lat},{lng}&key={GEO_KEY}')
    decoder = requests.get(GEO_URL)
    dJSON = decoder.json()

    if dJSON['status'] == 'OK':

        address = dJSON['results'][0]['address_components']
        #         print(dJSON)
        for component in address:
            if 'locality' in component['types']:
                return component['long_name']

    return None


def reverseGeoCityCountry(lat, lng):
    GEO_URL = ('https://maps.googleapis.com/maps/api/geocode/json?'
               f'latlng={lat},{lng}&key={GEO_KEY}')
    decoder = requests.get(GEO_URL)
    dJSON = decoder.json()

    if dJSON['status'] == 'OK':

        address = dJSON['results'][0]['address_components']
        name = ''

        for component in address:
            if 'locality' in component['types']:
                name += component['long_name'] + ", "

        for component in address:
            if 'administrative_area_level_1' in component['types']:
                name += component['long_name'] + ", "

        for component in address:
            if 'country' in component['types']:
                name += component['long_name']

        return name

    return None


def getGeocode(location):
    GEO_URL = ('https://maps.googleapis.com/maps/api/geocode/json?'
               f'address={location}&key={GEO_KEY}')
    decoder = requests.get(GEO_URL)
    dJSON = decoder.json()

    if dJSON['status'] == 'OK':

        address = dJSON['results'][0]['address_components']
        name = ''

        for component in address:
            if 'locality' in component['types']:
                name += component['long_name'] + ", "

        for component in address:
            if 'administrative_area_level_1' in component['types']:
                name += component['long_name'] + ", "

        for component in address:
            if 'country' in component['types']:
                name += component['long_name']

        geoloc = dJSON['results'][0]['geometry']['location']
        return [geoloc['lat'], geoloc['lng'], name]

    return None


def getManyIATA(coords):
    IATA_URL = ('https://api.lufthansa.com/v1/references/airports/nearest/'
                f'{coords[0]},{coords[1]}')
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
    print('Coordinates:', coords)
    print('Bad IATA >:( ->', getIATA(coords))
    print('Good IATA ->', getManyIATA(coords))

    print("Reverse geocode:", reverseGeoCityCountry(coords[0], coords[1]))


if __name__ == "__main__":
    main()
