import json
import ast
import pandas as pd
import requests
url = "http://localhost:8080/api/vi/empdata"
headers = {
    'cache-control': "no-cache",
    'postman-token': "72c97887-727e-ae9e-36ed-182f725fb6b5"
    }
response = requests.request("GET", url, headers=headers)
print(response.text)
mystr = response.text
val = ast.literal_eval(mystr)
val1 = json.loads(json.dumps(val))
val2 = val1['tags'][0]['results'][0]['values']
print pd.DataFrame(val2, columns=["name", "address"])
