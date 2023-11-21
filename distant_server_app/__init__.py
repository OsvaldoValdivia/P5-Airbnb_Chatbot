from flask import Flask, request
import services
import json
import requests
 
app = Flask(__name__)
 
with open('distant_server_app/config.json') as f:
    config = json.load(f)
 
app.config.update(config)
 
 
@app.route('/', methods=['GET'])
def welcome():
    return 'Distant server online to connect with Meta API'
    

@app.route('/webhook/', methods=['GET'])
def verify_token():
    try :
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        print('WEBHOOK_TOKEN',app.config['WEBHOOK_TOKEN'])

        if token == app.config['WEBHOOK_TOKEN'] and challenge != None:
            return challenge
        else : 
            return 'token incorrecto',403

    except Exception as e:
        return e,403


@app.route('/webhook/', methods=['POST'])
def receive_message():
    try :
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.get_message_whatsapp(message) # Server Received message 

        response_whatsapp = call_aws(text)
        print('Message from', number)
        services.administrate_chatbot(response_whatsapp, number, messageId, name)

        print('enviado')
        return 'enviado'

    except Exception as e:
        return 'no enviado'+ str(e)
    
def call_aws(message):
    headers = {
        "Content-Type": "application/json;charset=utf-8",
        'Accept-Charset': 'UTF-8',
        'Accept': '*/*'
    }
    url = 'https://42bf-176-166-43-90.ngrok-free.app/'+str(message)

    response = requests.get(url, headers = headers)

    print(response.json())

    return str(response.json())

if __name__ == '__main__':
    app.run(debug=True)