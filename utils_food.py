import zomatopy
from wit import Wit 
Zomato_API_Key = "53305a201a741cf7de0fc4e313a79f02"
zomato = zomatopy.initialize_app(Zomato_API_Key)
category_dictionary = zomato.get_categories()

def wit_response_food(message_text):
	access_token = "V2RDH2426FJN6TH6H5GBS36F2FAKLPC5"
	client = Wit(access_token = access_token)
	resp = client.message(message_text)
	categories = {'Occasion':None, 'Cuisine':None, 'location':None}
	entities = list(resp['entities'])
	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']
	return categories

def getRestaurantInfo(message_text):
	entities = wit_response_food(message_text)
	queryCuisineID=""
	queryCategoryID=""
	location_metadata = zomato.get_locationID(entities['location']) #getting locationID
	location_id = location_metadata['location_suggestions'][0]['entity_id']
	location_type = location_metadata['location_suggestions'][0]['entity_type']
	cityID = location_metadata['location_suggestions'][0]['city_id']
	lat = location_metadata['location_suggestions'][0]['latitude']
	lon = location_metadata['location_suggestions'][0]['longitude']
	cuisine_metadata = zomato.get_cuisines(cityID, lat, lon)
	if entities['Cuisine']!=None:
		for cuisineID in cuisine_metadata:
			if entities['Cuisine'].lower() == (cuisine_metadata[cuisineID]).lower():
				break
		queryCuisineID = cuisineID
	if entities['Occasion']!=None:
		for catID in category_dictionary:
			if entities['Occasion'].lower() == (category_dictionary[catID]).lower():
				break		
		queryCategoryID = catID
	resID_metadata = zomato.restaurant_search("",location_id,location_type,queryCuisineID,queryCategoryID,lat,lon)
	elements = []
	for item in resID_metadata:
		element = {
					'title': item['name'],
					'buttons': [{
								'type': 'web_url',
								'title': "View in Zomato",
								'url': (item['url']).replace('\/','/')
					}],
					'image_url': (item['image_url']).replace('\/','/')		
		}
		elements.append(element)
	return elements