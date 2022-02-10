#!/bin/bash

curl -v -XPOST -H 'Content-type: application/json' -d '{"bookid":"254","title":"Testing Python With Bash Unit Testing","description":"lamest book ever","authors":'Bertrand K',"isbn":"123456789ABC"}' http://localhost:8080/api/add_book
