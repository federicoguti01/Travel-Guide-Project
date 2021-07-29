import requests

AUTH_KEY = 'AIzaSyA8jYYYxddQbrHHI-9jPUWIVe3O_69nP0A'

def getGeocode(location):
    GEO_URL = f'https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={AUTH_KEY}'
    decoder = requests.get(GEO_URL)
    dJSON = decoder.json()


    geoloc = dJSON['results'][0]['geometry']['location']
    return [geoloc['lat'], geoloc['lng']]


def main():
    location = input('Enter a location: ')
    print(getGeocode(location))


if __name__ == "__main__":
    main()
