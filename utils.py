from secretsLol import DATA_DIRECTORY
import csv

def jsonToCSV(fileName, showName, jsonObj):
    filePath = DATA_DIRECTORY + showName + fileName

    headers = []
    for obj in jsonObj:
        headers = obj.keys()
        break

    with open(filePath, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        # there was an error where some guest characters didn't have
        # the correct headers in order to write to csv
        # added missing headers and then put it in order
        # probably better way but ¯\_(ツ)_/¯
        for obj in jsonObj:
            if len(obj.keys()) != len(headers):
                for header in headers:
                    if header not in obj.keys():
                        obj[header] = ""
                newObj = {
                    "character": obj["character"],
                    "credit_id": obj["credit_id"],
                    "order": obj["order"],
                    "adult": obj["adult"],
                    "gender": obj["gender"],
                    "id": obj["id"],
                    "known_for_department": obj["known_for_department"],
                    "name": obj["name"],
                    "original_name": obj["original_name"],
                    "popularity": obj["popularity"],
                    "profile_path": obj["profile_path"],
                    "episodeId": obj["episodeId"],
                    "seasonNumber": obj["seasonNumber"],
                    "episodeNumber": obj["episodeNumber"]
                }
                writer.writerow(newObj)
            else:
                writer.writerow(obj)
    
def jsonDump(fileName, jsonObj):
    with open(fileName, "w") as f:
        json.dump(jsonObj, f)