import random
import json
import torch
import sys
import os

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))
model_files = os.path.abspath(os.path.join(os.path.dirname(__file__),'../model_files'))

# Add the parent directory to sys.path
sys.path.append(parent_dir)
sys.path.append(model_files)

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

class Bot:

    def __init__(self):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        with open(model_files+'/intents.json','r', encoding='utf-8') as f:
            self.intents = json.load(f)

        FILE = model_files+'/data.path'
        data = torch.load(FILE)


        # Retrieve model parameters
        input_size = data['input_size']
        hidden_size = data['hidden_size']
        output_size = data['output_size']
        self.all_words = data['all_words']
        self.tags = data['tags']
        model_state = data['model_state']

        # Recreate model
        self.model = NeuralNet(input_size, hidden_size, output_size).to(device)
        self.model.load_state_dict(model_state)
        self.model.eval()


    def get_response(self,request_text):

        tokenized_sentence = tokenize(request_text)
        X = bag_of_words(tokenized_sentence, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X)

        output = self.model(X)
        _ , predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        # Get probability of the response
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75 :
            for intent in self.intents['intents'] : 
                if tag == intent['tag'] : 
                    resp = str(random.choice(intent['responses']))
        else : 
            resp = "Disculpa, no te entendí"

        return str(resp)