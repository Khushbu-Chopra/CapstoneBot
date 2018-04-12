import os, sys
from flask import Flask, request
from utils_main import wit_response_main
from pymessenger import Bot

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAcaPHRpfHgBAIGA0B5fF6f01XDOBXI6CiFGo1TxSRfU0mq7JbVxPVHZAQaaSm9ZCpGMVvLnZBtHDZCwp1eI38fVKucenu9K4APOpB8caYO09yvZBUrGtnCaV0gsHXNP41EaTfmGvKwE2oDeW3iCNWGCqxmgXTSiyVTRSFszBDvuxm26fQa9v"

bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
	# Webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
		if not request.args.get("hub.verify_token") == "hello":
			return "Verification token mismatch", 403
		return request.args["hub.challenge"], 200
	return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
	data = request.get_json()
	log(data)

	if data['object'] == 'page':
		for entry in data['entry']:
			for messaging_event in entry['messaging']:

				# IDs
				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):
					# Extracting text message
					if 'text' in messaging_event['message']:
						messaging_text = messaging_event['message']['text']
					else:
						messaging_text = 'no text'
					categories = wit_response_main(messaging_text)
					if(categories['greetings']!=None):
						response = "Hey!"
						bot.send_text_message(sender_id,response)
					elif(categories['AboutMe']!=None):
							response = "\nI am your AssistBot. I am here to help you :) \nI can assist you with daily news, weather forecasts, restaurants information and general queries."
							bot.send_text_message(sender_id,response)
					elif(categories['NewsBot']!= None):
						from utils import wit_response, get_news_elements
						categories1 = wit_response(messaging_text)
						elements = get_news_elements(categories1)
						bot.send_generic_message(sender_id, elements)
					elif(categories['FoodBot']!= None):
						from utils_food import getRestaurantInfo
						elements = getRestaurantInfo(messaging_text)
						bot.send_text_message(sender_id, "While you are here, you must check out these restaurants!\n")
						bot.send_generic_message(sender_id, elements)
					elif(categories['gkBot']!= None):
						import general_knowledge
						response_gk = general_knowledge.main(messaging_text)
						bot.send_text_message(sender_id,response_gk)
					elif(categories['WeatherBot']!= None):
						from utils_weather import wit_response, get_weather
						response_weather = get_weather(messaging_text)
						bot.send_text_message(sender_id,response_weather)
					else:
						bot.send_text_message(sender_id,"I'm not sure what are you saying!")

	return "ok", 200

def log(message):
	print(message)
	sys.stdout.flush()


if __name__ == "__main__":
	app.run(debug = True, port = 40)