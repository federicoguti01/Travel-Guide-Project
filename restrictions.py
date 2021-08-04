import requests
from geocoding import getGeocode, getManyIATA
import pandas as pd
from config import AUTH_KEY


def getRestrictions(destination):

    #     originCoords = getGeocode(origin)
    #     destCoords = getGeocode(destination)

    #     originIATA = getIATA(originCoords)
    destIATA = getManyIATA(destination)

    URL = 'https://covid-api.thinklumo.com/data?airport='

    headers = {
        "x-api-key": AUTH_KEY
    }

    for iata in destIATA:
        decoder = requests.get(URL + iata, headers=headers)
        if decoder.status_code == 200:
            dJSON = decoder.json()
#             print(dJSON)
            return dJSON

    return None


def getAdvisoryDF(dJSON):
    df = pd.json_normalize(dJSON['travel_advisories'])

    FIELDS = ["issued_by", "advisory", "url", "last_updated"]

    return df[FIELDS]


def getCountryName(dJSON):
    return dJSON['airport']['country_name']


def getChartUrl(dJSON):
    if dJSON['covid_stats']['county_district'] is not None:
        return {
            "county": dJSON['covid_stats']['county_district']['chart_url'],
            "state": dJSON['covid_stats']['state_province']['chart_url'],
            "country": dJSON['covid_stats']['country']['chart_url']
        }

    if dJSON['covid_stats']['state_province'] is not None:
        return {
            "state": dJSON['covid_stats']['state_province']['chart_url'],
            "country": dJSON['covid_stats']['country']['chart_url']
        }

    return {
        "country": dJSON['covid_stats']['country']['chart_url']
    }


def getRiskLevel(dJSON):
    return dJSON['covid_stats']['country']['risk_rating']['risk_level'].upper()


def getEntryExitDF(dJSON):
    df = pd.json_normalize(dJSON['covid_info']['entry_exit_info'])

    FIELDS = [
        "source",
        "quarantine",
        "testing",
        "travel_restrictions",
        "last_updated"]

    return df


def main():
    destination = input('Enter a destination: ')
    loc = getGeocode(destination)
    jsonResponse = getRestrictions(loc)
#     print(jsonResponse)
    if(jsonResponse is not None):
        # more options can be specified also
        with pd.option_context('display.max_rows', None, 'display.max_columns',
                               None):
            print(getAdvisoryDF(jsonResponse))
            print(getEntryExitDF(jsonResponse))
        print("Covid Data Chart(s):", getChartUrl(jsonResponse))
        print("Risk Level:", getRiskLevel(jsonResponse))
    else:
        print('No information could be retrieved.')


if __name__ == "__main__":
    main()
