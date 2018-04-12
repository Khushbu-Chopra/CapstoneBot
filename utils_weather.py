from weather import Weather, Unit
from wit import Wit
weather = Weather(unit=Unit.CELSIUS)
def wit_response(message_text):
	access_token = "XEXDABCV7AHNSQ77GKYONBME635V2YES"
	client = Wit(access_token = access_token)
	resp = client.message(message_text)
	categories = {'datetime':None, 'location':None}
	entities = list(resp['entities'])
	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']
	return categories

def get_weather(message_text):
	categories = wit_response(message_text)
	location = weather.lookup_by_location(categories['location'])
	forecasts = location.forecast
	condition = location.condition
	
	return ((categories['location']).title() + " is " + condition.text + " with Maximum Temperature: " + forecasts[0].high + "C and Minimum Temperature: " + forecasts[0].low + "C")
