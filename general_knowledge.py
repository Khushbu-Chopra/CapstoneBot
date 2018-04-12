import sys
import wolframalpha
import wikipedia
from wit import Wit 
def wit_response_gk(message_text):
    access_token = "QCPVR3VQZQ5VP6LVMEMOVRTVBXWEVVWX"
    client1 = Wit(access_token = access_token)
    resp = client1.message(message_text)
    categories = {'topic': None}
    entities = list(resp['entities'])
    for entity in entities:
        categories[entity] = resp['entities'][entity][0]['value']
    return categories
def main(messaging_text):
    client = wolframalpha.Client("V63VYX-EX865W38Y4")
    res = client.query(messaging_text)
    #print((res.results).text)
    try:
        return next(res.results).text
    except (StopIteration, AttributeError) as e: 
        #category = wit_response_gk(messaging_text)
        page = wikipedia.page(messaging_text)
        pageUrl=page.url
        summary = wikipedia.summary(messaging_text, sentences=1)
        response = summary + "\nRead more here: \n" + pageUrl
    return response