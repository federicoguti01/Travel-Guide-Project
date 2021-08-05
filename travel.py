import requests
from geocoding import getGeocode
from geocoding import getManyIATA
from geocoding import reverseGeocode
from geocoding import reverseGeoCity
from config import headers

global min_price
global max_price


def travel_search(location):
    try:
        url = "https://travel-advisor.p.rapidapi.com/locations/search"
        # user_input = input(
        # "Please enter the location to which you would like to travel: \n")
        querystring = {
            "query": location,
            "limit": "30",
            "offset": "0",
                      "units": "km",
                      "location_id": "1",
                      "currency": "USD",
                      "sort": "relevance",
                      "lang": "en_US"}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        return parse_travel_search(response.json())
    except BaseException:
        return "No information is currently available for the inputted location. Please ensure your spelling is correct and try again.\n"


def parse_travel_search(file_name):
    results = {}
    new_list = []
    results['Name'] = file_name['data'][0]['result_object']['name']
    try:
        results['Country'] = file_name['data'][0]['result_object']['ancestors'][1]['name']
    except BaseException:
        pass
    results['Latitude'] = file_name['data'][0]['result_object']['latitude']
    results['Longitude'] = file_name['data'][0]['result_object']['longitude']
    # try:
    # results['Night Life'] = file_name['data'][0]['result_object']['category_counts']['attractions']['nightlife']
    # except BaseException:
    # pass
    results['Description'] = file_name['data'][0]['result_object']['geo_description']
    results['Image'] = file_name['data'][0]['result_object']['photo']['images']['original']['url']

    return results


def first_search(latitude, longitude, adults, rooms, checkin, nights):
    url = "https://travel-advisor.p.rapidapi.com/hotels/list-by-latlng"
    querystring = {
        "latitude": latitude,
        "longitude": longitude,
        "lang": "en_US",
        "limit": "5",
        "adults": adults,
        "rooms": rooms,
        "currency": "USD",
        "checkin": checkin,
        "subcategory": "hotel,bb,specialty",
        "nights": nights}

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


def hotel_search(latitude, longitude, adults, rooms,
                 checkin, nights, min_price, max_price):
    try:
        url = "https://travel-advisor.p.rapidapi.com/hotels/list-by-latlng"
        first_search(latitude, longitude, adults, rooms, checkin, nights)
        querystring = {
            "latitude": latitude,
            "longitude": longitude,
            "lang": "en_US",
            "limit": "5",
            "adults": adults,
            "rooms": rooms,
            "currency": "USD",
            "checkin": checkin,
            "subcategory": "hotel,bb,specialty",
            "nights": nights}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        return parse_hotel_search(response.json(), min_price, max_price)
    except BaseException:
        return "No hotels could be found for your search. Please try again.\n"


def parse_hotel_search(file_name, min_price, max_price):
    results = {}
    my_list = []
    hotel_count = 0

    if file_name['data'] == []:
        return None

    for hotel in range(0, 5):
        if int(min_price) > int(file_name['data'][hotel]['hac_offers']['offers'][0]['display_price_int']) or int(
                max_price) < int(file_name['data'][hotel]['hac_offers']['offers'][0]['display_price_int']):
            pass
        else:
            results['Name'] = file_name['data'][hotel]['name']
            Latitude = file_name['data'][hotel]['latitude']
            Longitude = file_name['data'][hotel]['longitude']
            results['Address'] = reverseGeocode(Latitude, Longitude)
            try:
                results['Price'] = file_name['data'][hotel]['price']  # per night
            except BaseException:
                results['Price'] = "Price information not available"
            results['Availability'] = file_name['data'][hotel]['hac_offers']['availability'].upper()
            try:
                results['Offer Price'] = file_name['data'][hotel]['hac_offers']['offers'][0]['display_price']
                results['Offer Link'] = file_name['data'][hotel]['hac_offers']['offers'][0]['link']
            except BaseException:
                results['Offer Price'] = "No offers currently available"

            results['Tier'] = int(
                float(file_name['data'][hotel]['hotel_class']))

            # print(file_name['data'][4])

            try:
                results['Rating'] = file_name['data'][hotel]['raw_ranking'][:4]
            # except KeyError:
            # using rating (rounded) instead of raw_ranking because some hotels
            # do not have a raw_ranking field
                # results['Rating'] = file_name['data'][hotel]['rating']
            except BaseException:
                results['Rating'] = "No ratings are currently available"

            results['NumReviews'] = file_name['data'][hotel]['num_reviews']

            try:
                results['Cancellation Policy'] = file_name['data'][hotel]['hac_offers']['offers'][0]['free_cancellation_detail']
            except BaseException:
                results['Cancellation Policy'] = "This hotel does not offer a free cancellation policy"

            try:
                results['Image'] = file_name['data'][hotel]['photo']['images']['original']['url']
            except BaseException:
                results['Image'] = ('https://intersections.humanities.ufl.edu/wp-content/u'
                                    'ploads/2020/07/112815904-stock-vector-no-image-av'
                                    'ailable-icon-flat-vector-illustration-1.jpg')

            my_list.append(results.copy())
    return my_list


def flight_search(lat, lang, depart, adults, date):
    # my_var = travel_search()
    # destination_name = my_var['Name']
    # home_input = input("Please enter the location to which you are departing from: \n")
    # departure_date = input("When would you like to depart? Please enter in the following format: YYYY-MM-DD\n")
    # num_adults = input("How many adults will be traveling?: \n")
    # try:
    #     val = int(num_adults)
    # except ValueError:
    #     num_adults = 1
    #    print("That's not a number, we will assume one adult is traveling")
    home_airport_coor = getGeocode(depart)
    home_airport_code = getManyIATA(home_airport_coor)
    arrival_airport_address = reverseGeocode(home_airport_coor[0], home_airport_coor[1])
    destination_name = reverseGeoCity(lat, lang)
    destination_airport_coor = getGeocode(destination_name)
    destination_airpot_code = getManyIATA(destination_airport_coor) 
    depart_airport_address = reverseGeocode(lat, lang)
    url = "https://travel-advisor.p.rapidapi.com/flights/create-session"
    try:
        querystring = {
            "o1": home_airport_code,
            "d1": destination_airpot_code,
            "dd1": date,
            "currency": "USD",
            "ta": adults}
        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        return parse_flights_search(response.json())
    except BaseException:
        print("Invalid Response")
    print(response.json)
    return parse_flights_search(response.json(), arrival_airport_address, depart_airport_address)


def parse_flights_search(file_name, arrivalAirportAddress, departAirportAddress):
    results = {}
    results['URL'] = file_name['search_url']
    results['Departing From'] = file_name['airports'][1]['n']
    results['Departing Airport Address'] = departAirportAddress
    results['Arrival To'] = file_name['airports'][0]['n']
    results['Arrival Airport Address'] = arrivalAirportAddress 
    print(results)
    return results


def attractions_search(location):
    url = "https://travel-advisor.p.rapidapi.com/attractions/list-by-latlng"
    geo_var = getGeocode(location)
    latitude = geo_var[0]
    longitude = geo_var[1]
    querystring = {
        "longitude": longitude,
        "latitude": latitude,
        "lunit": "mi",
        "currency": "USD",
        "lang": "en_US"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    location_id = 0
    count = 0
    try:
        while (int(location_id) == int(0)):
            location_id = response.json()['data'][count]['location_id']
            count += 1
    except BaseException:
        print("No locations found! Please try again. ")

    # return response.json()
    return attraction_details(location_id)


def attraction_details(location_id):
    url = "https://travel-advisor.p.rapidapi.com/attractions/get-details"
    querystring = {
        "location_id": location_id,
        "currency": "USD",
        "lang": "en_US"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    return parse_attraction_details(response.json())


def parse_attraction_details(file_name):
    results = {}
    my_list = []

    results['Name'] = file_name['name']
    results['Latitude'] = file_name['latitude']
    results['Longitude'] = file_name['longitude']

    try:
        results['Image'] = file_name['photo']['images']['original']['url']
    except BaseException:
        results['Image'] = "No images available"

    results['Description'] = file_name['description']
    results['URL'] = file_name['web_url']
    try:
        results['Rating'] = file_name['raw_ranking']
    except BaseException:
        results['Rating'] = file_name['rating']

    return results


if __name__ == '__main__':
    # print(travel_search("France"))
    # print(hotel_search(51.51924, -0.096654, 4, 2, "2021-10-11", 3, 100, 300))
    # print(attractions_search("Berlin"))
    flight_search(51.51924, -0.096654, "Dallas", 3, "2021-12-25")
