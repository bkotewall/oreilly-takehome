#!/usr/bin/python3

# curl -v -XPOST -H 'Content-type: application/json' -d '{"bookid":"254","title":"Testing Python With Bash Unit Testing","description":"lamest book ever","authors":'Bertrand K',"isbn":"123456789ABC"}' http://localhost:8080/api/add_book

import json
import requests

data = { "bookid":255,
         "title":"Testing Python With Bash Unit Testing 2nd ed",
         "description":"lamest book ever",
         "authors": ['Bertrand K'],
         "isbn":"123456789ABCD"}
data_json = json.dumps(data)
print(data_json)
# payload = {'json_payload': data_json }
r = requests.post('http://127.0.0.1:8080/api/add_book', json=data_json)
print(r.status_code)
print(r.json)

wrong_data = { "bookid": "123" }
data_json=json.dumps(wrong_data)
r = requests.post('http://127.0.0.1:8080/api/add_book', json=data_json)

