import json
import yaml
import sqlite_utils
import os

YAMLDIR = "yml"
PK = "id"

def extractData(newKey, data, requiredFields):
    flatData = []
    for key in requiredFields.keys():
        if key in data.keys():
            rf = requiredFields[key]

            if isinstance(rf, dict):
                flatData = flatData + extractData(f"{newKey}{key}-", data[key], rf)
            else:
                for field in rf:
                    if field in data[key].keys():
                        flatData.append((f"{newKey}{key}-{field}", data[key][field]))

    return flatData

def transformData(yamlData, requiredFields):
    jsonData = []
    for id, (filename, data) in enumerate(yamlData):
        newJson = {"id": id, "file": filename}
        print(extractData("", data, requiredFields))
        

def main():
    # Get all yaml data
    yamlData = []
    for filename in os.listdir(YAMLDIR):
        fp = os.path.join(YAMLDIR, filename)
        
        with open(fp, "r") as f:
            for data in yaml.safe_load_all(f):
                yamlData.append((filename, data))

    # Get the fields we want in the database
    with open("requiredFields.json", "r") as f:
        requiredFields = json.load(f)

    transformData(yamlData, requiredFields)
    
if __name__ == "__main__":
    main()