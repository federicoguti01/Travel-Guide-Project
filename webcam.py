import requests
from geocoding import getGeocode
from config import CAM_KEY


headers = {
    "x-windy-key": CAM_KEY
}

def getWebcam(location):
    URL = ('https://api.windy.com/api/webcams/v2/list/nearby='
           f'{str(location[0])},{str(location[1])}'
           ',100/?show=webcams:location,url')

    decoder = requests.get(URL, headers=headers).json()
    return decoder
  
def getWebLink(decoder):
    total = decoder['result']['total']
    webcams = decoder['result']['webcams']
    x = []
    for webcam in webcams:
        x.append(webcam['url']['current']['desktop'])
    print(decoder)
    return x
  
def getTitle(decoder):
    total = decoder['result']['total']
    webcams = decoder['result']['webcams']
    x = []
    for webcam in webcams:
        x.append(webcam['title'])
    return x
  
def main():
    location = input('Enter a location: ')
    coordinates = getGeocode(location)
    decoder = getWebcam(coordinates)
    print(getWebLink(decoder))
    print(getTitle(decoder))

if __name__ == "__main__":
    main()
