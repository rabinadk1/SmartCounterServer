# import requests
#
# r = requests.post("http://localhost:5000/api/updateseat",
#                   json={"CustomerName": "Suke", "Contact": 9880112342, "Seats": ["a2", "a3"], "BusId": 2})
# # r = requests.get("http://localhost:5000/api")

import json
filename = "buses.json"
with open(filename, 'r') as outfile:
    data = json.loads(outfile.read())  # converts json to dict
    print(data)