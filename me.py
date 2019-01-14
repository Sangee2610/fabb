import json
import requests
import tabulate
import ast

url = "http://localhost:8080/api/vi/empdata"
headers = {
    'cache-control': "no-cache",
    'postman-token': "72c97887-727e-ae9e-36ed-182f725fb6b5"
    }
response = requests.request("GET", url, headers=headers)
data = json.loads(response.text)
ult_list = ast.literal_eval(json.dumps(data))
header = ult_list[0].keys()
rows =  [x.values() for x in ult_list]
print(tabulate.tabulate(rows, header))
print(tabulate.tabulate(rows, header, tablefmt='grid'))
print(tabulate.tabulate(rows, header, tablefmt='rst'))

