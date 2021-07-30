import requests
from dummy import my_var
from hotel import hotel_info
from geocoding import getGeocode
from geocoding import getManyIATA
#from flights import flight_var
from new_hotel import new_hotel

headers = {
    'content-type': "application/json",
    'x-rapidapi-key': "f888c871b1msh73f2e40214b8958p1399c0jsneedeb80a5574",
    'x-rapidapi-host': "travel-advisor.p.rapidapi.com"
}


def travel_search():
    try:
        url = "https://travel-advisor.p.rapidapi.com/locations/search"
        user_input = input(
            "Please enter the location to which you would like to travel: \n")
        querystring = {
            "query": user_input,
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
        return "Unable to find location. Please ensure that your spelling is correct and try again!"


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
    results['Night Life'] = file_name['data'][0]['result_object']['category_counts']['attractions']['nightlife']
    results['Description'] = file_name['data'][0]['result_object']['geo_description']
    results['Image'] = file_name['data'][0]['result_object']['photo']['images']['original']['url']

    return results


def hotel_search():
    url = "https://travel-advisor.p.rapidapi.com/hotels/list-by-latlng"
    my_var = travel_search()
    latitude = my_var['Latitude']
    longitude = my_var['Longitude']
    adults = input("How many adults will be staying?\n")
    rooms = input("How many rooms would you like?\n")
    checkin = input(
        "When would you like to check in? Please enter in the following format: YYYY-MM-DD\n")
    nights = input("How many nights would you like to stay?\n")
    min_price = input("Please enter your minimum price per night\n")
    max_price = input("Please enter your maximum price per night\n")

    querystring = {
        "latitude": latitude,
        "longitude": longitude,
        "lang": "en_US",
        "limit": "5",
        "adults": adults,
        "rooms": rooms,
        "pricesmin": min_price,
        "pricesmax": max_price,
        "currency": "USD",
        "checkin": checkin,
        "subcategory": "hotel,bb,specialty",
        "nights": nights}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    return parse_hotel_search(response.json())


def parse_hotel_search(file_name):
	results = {}
	my_list = []
	hotel_count = 0

	for hotel in range(0, 5):
		results['Name'] = file_name['data'][hotel]['name']
		results['Latitude'] = file_name['data'][hotel]['latitude']
		results['Longitude'] = file_name['data'][hotel]['longitude']
		results['Price Range (/night)'] = file_name['data'][hotel]['price']
		results['Availability'] = file_name['data'][hotel]['hac_offers']['availability']
		try:
			results['Offer Price'] = file_name['data'][hotel]['hac_offers']['offers'][0]['display_price']
			results['Offer Link'] = file_name['data'][hotel]['hac_offers']['offers'][0]['link']
		except BaseException:
			results['Offer Price'] = "No offers currently available"

		results['Tier(/5)'] = file_name['data'][hotel]['hotel_class']

		try:
			results['Rating'] = file_name['data'][hotel]['raw_ranking'][:4]
		except BaseException:
		# using rating (rounded) instead of raw_ranking because some hotels
		# do not have a raw_ranking field
			results['Rating'] = file_name['data'][hotel]['rating']

		results['Number of Reviews'] = file_name['data'][hotel]['num_reviews']

		try:
			results['Cancellation Policy'] = file_name['data'][hotel]['hac_offers']['offers'][0]['free_cancellation_detail']
		except BaseException:
			results['Cancellation Policy'] = "This hotel does not offer a free cancellation policy"

		my_list.append(results.copy())

	return my_list


def flight_search():
    my_var = travel_search()
    destination_name = my_var['Name']
    home_input = input(
        "Please enter the location to which you are departing from: \n")
    departure_date = input(
        "When would you like to depart? Please enter in the following format: YYYY-MM-DD\n")
    home_airport_coor = getGeocode(home_input)
    home_airport_code = getManyIATA(home_airport_coor)
    destination_airport_coor = getGeocode(destination_name)
    destination_airpot_code = getManyIATA(destination_airport_coor)
    url = "https://travel-advisor.p.rapidapi.com/flights/create-session"
    querystring = {
        "o1": home_airport_code,
        "d1": destination_airpot_code,
        "dd1": departure_date}

    #querystring = {"o1":home_airport_code,"d1":destination_airpot_code,"dd1":departure_date,"currency":"USD","ta":"1","c":"0"}
    response = requests.request(
        "GET", url, headers=headers, params=querystring)
    return response.json()
	
	
"""	
def new_hotel_search():

	url = "https://hotels-com-provider.p.rapidapi.com/v1/hotels/nearby"
	my_var = travel_search()
	latitude = my_var['Latitude']
	longitude = my_var['Longitude']
	
	adults = input("How many adults will be staying?\n")
	rooms = input("How many rooms would you like?\n")
	checkin = input(
			"When would you like to check in? Please enter in the following format: YYYY-MM-DD\n")
	nights = input("How many nights would you like to stay?\n")
	min_price = input("Please enter your minimum price per night\n")
	max_price = input("Please enter your maximum price per night\n")
	
	querystring = {"latitude":latitude,"checkin_date":"2022-08-26","locale":"en_US","adults_number":"1","sort_order":"STAR_RATING_HIGHEST_FIRST","currency":"USD","checkout_date":"2022-08-27","longitude":longitude,"guest_rating_min":"4","price_max":"500","amenity_ids":"527,2063","accommodation_ids":"20,8,15,5,1","theme_ids":"14,27,25","children_ages":"4,0,15","star_rating_ids":"3,4,5","page_number":"1","price_min":"10"}

	headers = {
			'x-rapidapi-key': "835ea1863cmsh8ec245f12ad64bap187695jsn701aabefa0f1",
			'x-rapidapi-host': "hotels-com-provider.p.rapidapi.com"
			}

	response = requests.request("GET", url, headers=headers, params=querystring)
	return parse_new_hotel_search(response.json())


def parse_new_hotel_search(file_name):
	results = {}
	my_list = []
	
	for hotel in file_name['searchResults']['results']:
		results['Name'] = hotel['name']
		my_list.append(results.copy())
	
	return my_list
"""	


if __name__ == '__main__':
	print(hotel_search())
	#print(new_hotel_search())
	#print(parse_new_hotel_search(new_hotel))
	#print(travel_search())
