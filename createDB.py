import json
import yaml
import sqlite_utils
import os
import sys

# Recursively iterate over all values in data that we want.
# We return a flattened list of this data with new keys 
# that sum the entire path of keys to that value.
#
# param:
#   newKey, string that represents the parent keys
#   data, the data from which we want to extract the values
#   requiredFields, specifies the data that we are interested in
#
# returns:
#   flattened list of tuples that contain a (new) key value pair
def extractData(newKey: str, data:dict, requiredFields:dict) -> list[tuple]:
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

# Get all the relevant data from all the yaml data
#
# param:
#   yamlData, contains the data from all the yaml files that we want to process
#   requiredFields, contains the fields that we want to extract from the yaml data
#
# returns:
#    list of dicts, where each dict corresponds to one entry in the database
def transformData(yamlData:list[tuple], requiredFields:dict) -> list[dict]:
    dictData = []
    for id, (filename, data) in enumerate(yamlData):
        newDict = {"id": id, "file": filename}
        for key, value in extractData("", data, requiredFields):
            newDict[key] = value
        
        dictData.append(newDict)
    
    return dictData


def main():
    pathToBaseDir = sys.argv[1]
    # Get settings from config file
    with open(os.path.join(pathToBaseDir, "config.json"), "r") as f:
        config = json.load(f)

    # Get all yaml data
    yamlData = []
    ymlDir = os.path.join(pathToBaseDir, config["yamlPath"])
    for filename in os.listdir(ymlDir):
        fp = os.path.join(ymlDir, filename)
        
        with open(fp, "r") as f:
            for data in yaml.safe_load_all(f):
                yamlData.append((filename, data))

    dictData = transformData(yamlData, config["requiredFields"])

    db = sqlite_utils.Database(config["dbName"], recreate=True)
    db[config["tableName"]].upsert_all(dictData, pk=config["pk"], alter=True)


if __name__ == "__main__":
    main()