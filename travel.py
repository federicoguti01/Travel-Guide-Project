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

global min_price
global max_price



def travel_search():
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
    #try:
		#results['Night Life'] = file_name['data'][0]['result_object']['category_counts']['attractions']['nightlife']
    #except BaseException:
		#pass
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
		
    return parse_hotel_search(response.json(), max_price)


def parse_hotel_search(file_name, max_price):
	results = {}
	my_list = []
	hotel_count = 0
	
	if file_name['data'] == []:
		return "No Search Results were found for your query. Please try again"

	for hotel in range(0, 5):
		#print("MAX PRICE: ", max_price, "\n PRICES: ", int(file_name['data'][hotel]['hac_offers']['offers'][0]['display_price'][1:]))
		if int(max_price) < int(file_name['data'][hotel]['hac_offers']['offers'][0]['display_price_int']):
			pass
		else:
			results['Name'] = file_name['data'][hotel]['name']
			results['Latitude'] = file_name['data'][hotel]['latitude']
			results['Longitude'] = file_name['data'][hotel]['longitude']
			try:
				results['Price Range (/night)'] = file_name['data'][hotel]['price']
			except:
				pass
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
    home_input = input("Please enter the location to which you are departing from: \n")
    departure_date = input("When would you like to depart? Please enter in the following format: YYYY-MM-DD\n")
    num_adults = input("How many adults will be traveling?: \n")
    try:
      val = int(num_adults)
    except ValueError:
      num_adults = 1
      print("That's not a number, we will assume one adult is traveling")
    home_airport_coor = getGeocode(home_input)
    home_airport_code = getManyIATA(home_airport_coor)
    destination_airport_coor = getGeocode(destination_name)
    destination_airpot_code = getManyIATA(destination_airport_coor)
    url = "https://travel-advisor.p.rapidapi.com/flights/create-session"
    try:
      querystring = {"o1":home_airport_code,"d1":destination_airpot_code,"dd1":departure_date,"currency":"USD","ta":num_adults}
      response = requests.request("GET", url, headers=headers, params=querystring)
      return parse_flights_search(response.json())
    except:
      print("Invalid Response")
    return parse_flights_search(response.json())
    
    

def parse_flights_search(file_name):
    results = {} 
    results['URL']= file_name['search_url']
    results['Departing From'] = file_name['airports'][1]['n']
    results['Arrival To'] = file_name['airports'][0]['n']
    return results
	


if __name__ == '__main__':
	#my_string = hotel_search()
	new_string = hotel_search()
	print(new_string)
	#print(new_hotel_search())
	#print(parse_new_hotel_search(new_hotel))
	#print(travel_search())
