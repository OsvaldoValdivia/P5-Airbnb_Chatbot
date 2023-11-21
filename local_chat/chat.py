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

 
# importing
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open(model_files+'/intents.json','r') as f:
    intents = json.load(f)

FILE = model_files+'/data.path'
data = torch.load(FILE)


# Retrieve model parameters
input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']
all_words = data['all_words']
tags = data['tags']
model_state = data['model_state']

# Recreate model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


bot_name = 'Jimbo'
print("Let's chat! Type 'quit' to exit")
while True:
    sentence = input("You : ")
    if sentence == "quit" : 
        break

    tokenized_sentence = tokenize(sentence)
    X = bag_of_words(tokenized_sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _ , predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Get probability of the response
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75 :
        for intent in intents['intents'] : 
            if tag == intent['tag'] : 
                print(f"Detected tag: {tag}, probability : {prob.item()}")
                print(f"{bot_name}: {random.choice(intent['responses'])}")
    else : 
        print(f"{bot_name}: Disculta, no entendi")