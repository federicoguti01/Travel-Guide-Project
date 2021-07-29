import requests
from dummy import my_var

headers = {
    'content-type': "application/json",
    'x-rapidapi-key': "f888c871b1msh73f2e40214b8958p1399c0jsneedeb80a5574",
    'x-rapidapi-host': "travel-advisor.p.rapidapi.com"
    }

def travel_search():
	
	url = "https://travel-advisor.p.rapidapi.com/locations/search"
	user_input = input("Please enter the location to which you would like to travel: \n")
	querystring = {"query":user_input,"limit":"30","offset":"0","units":"km","location_id":"1","currency":"USD","sort":"relevance","lang":"en_US"}
	response = requests.request("GET", url, headers=headers, params=querystring)
	return parse_travel_search(response.json())

	
def parse_travel_search(file_name):
	results = {}
	new_list = []
	results['Name'] = file_name['data'][0]['result_object']['name']
	results['Latitude'] = file_name['data'][0]['result_object']['latitude']
	results['Longitude'] = file_name['data'][0]['result_object']['longitude']
	results['Night Life'] = file_name['data'][0]['result_object']['category_counts']['attractions']['nightlife']
	results['Description'] = file_name['data'][0]['result_object']['geo_description']
	
	return results
	
	# for the hotels; should we index from here or call the hotel search ???
	for i in file_name['data']:
		pass


if __name__ == '__main__':
	print(travel_search())