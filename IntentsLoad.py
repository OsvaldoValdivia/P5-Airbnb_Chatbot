import json

class IntentsLoad:

    def __init__(self, json_files_paths_list):
        self.json_files_paths_list = json_files_paths_list

    def merge_jsons(self):
        open_jsons = []

        # Read files
        for path in self.json_files_paths_list:
            with open(path,'r',encoding='utf-8') as f:
                obj_json = json.load(f)
                open_jsons.append(obj_json)
        
        # Create merged json file
        output_json = {'intents':[]}

        for open_json in open_jsons:
            json_dict = open_json['intents']
            for intent in json_dict : 
                output_json['intents'].append(intent)


        with open('intents.json', 'w',encoding='utf-8') as output_file:
                json.dump(output_json, output_file, ensure_ascii=False)


i = IntentsLoad(["intents/intents_saludos.json",
                 "intents/intents_despedidas.json",
                 "intents/intents_estado.json"
                ])
i.merge_jsons()