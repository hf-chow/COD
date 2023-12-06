import json

def load_sample(json_file):
    with open(json_file) as file:
        resp = json.load(file)
    return resp

def get_keys(search_dict):
    keys = []
    for k, v in search_dict.items():
        keys.append(k)
        if isinstance(v, dict):
            keys.extend(get_keys(v))
    return keys


documentai_sample = "document-ocr.json"
textract_sample = "textract-ocr.json"

sample = load_sample(textract_sample)
keys = get_keys(sample)

types = []

for b in sample["Blocks"]:
    for i in b:
        for j in i:
            types.append(j["Type"])
