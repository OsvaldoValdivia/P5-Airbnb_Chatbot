import requests
from flask import current_app
import json

def get_message_whatsapp(message):
    if 'type' not in message :
        text = 'Mensaje no reconocido'
    else :
        typeMessage = message['type']
        if typeMessage == 'text':
            text = message['text']['body']
    
    return text


def send_message_whatsapp(data):
    try:
        headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
        }

        url = 'https://graph.facebook.com' + f"/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"
        response = requests.post(url, 
                                headers = headers,
                                data= data)
        print("Data:",data,"\n")
        if response.status_code == 200:
            return 'Mensaje enviado',200
        else:
            return 'Error al enviar mensaje',response.status_code

    except Exception as e:
        return e,403

    
def text_message(number, text):

  return json.dumps(
    {
        "messaging_product": "whatsapp",
        "preview_url": False,
        "recipient_type": "individual",
        "to": number,
        "type": "text",
        "text": {
            "body": text
        }
    }
  )


def administrate_chatbot(text, number, messageId, name):
    data = text_message(number, text)
    send_message_whatsapp(data)