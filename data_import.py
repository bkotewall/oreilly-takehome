from sqlalchemy import exc
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime
import json
import requests
import models

def request_url():
    url_root = 'https://learning.oreilly.com/api/v2/search/'
    query = '?limit=200&query=python'
    fields1 = '&fields=isbn&fields=authors&fields=title'
    fields2 = '&fields=description&fields=publishers&fields=format'
    url = url_root + query + fields1 + fields2
    return url


def insert_book(bk_id, bk_data, dbh):
    newbook = Book(id = bookid,
                   isbn = bk_data["isbn"],
                   authors = bk_data["authors"],
                   title = bk_data["title"],
                   description = bk_data["description"]
                  )
    try:
        dbh.add(newbook)
        dbh.commit()
        return True
    except exc.SQLAlchemyError as e:
        print(e)
        pass
        return False


def import_data():
    url = request_url()
    try:
        request_data = requests.get(url)
        response_json = request_data.json()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error happened: {err}")
    bdata_json = response_data["results"]
    bookid = 0
    for book_data in bdata_json:
        try:
            if book_data["format"] == "book":
                insert_book(bookid, book_data, db_session)
                print(book["publishers"])
            else:
                pass
        except KeyError as e:
            print(f'{book["title"]}, {e}')
