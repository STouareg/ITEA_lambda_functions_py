import json
from botocore.vendored import requests

TOKEN = 'telegrambot'
chat_id = 'adminchatid'

URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def send_message(text, chat_id):
    final_text = "You said: " + text
    url =  URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
    requests.get(url)


def lambda_handler(event, context):
    try:
       reply = 'lesson10'
   
    except: 
       reply = 'Not supported'    

    send_message(reply, chat_id)

    return { 
        'statusCode' : 200     
    }


