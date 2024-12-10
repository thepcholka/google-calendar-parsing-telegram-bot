import json

def push_to_json(json_name, file_to_push):
    with open(json_name, "w") as jsonfile:
        json.dump(file_to_push, jsonfile)

def take_from_json(json_name):
    with open(json_name) as jsonfil:
        jsonfile = json.load(jsonfil)
    return jsonfile
