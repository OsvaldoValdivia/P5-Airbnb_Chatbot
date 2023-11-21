from flask import Flask
from flask_restful import Resource, Api
from bot import Bot

app = Flask('ChatAPI')
api = Api(app)


class ChatBot(Resource):

    def __init__(self):
        self.bot = Bot()

    def get(self, message):
        resp = self.bot.get_response(message)
        print(resp.encode('utf-8', 'ignore').decode('utf-8'))
        return str(resp).encode('utf-8', 'ignore').decode('utf-8')
    
api.add_resource(ChatBot, '/<message>')

if __name__ == '__main__':
    app.run()