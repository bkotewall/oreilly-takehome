import json
import requests

url_root = 'https://learning.oreilly.com/api/v2/search/'
query = '?limit=200&query=python'
fields1 = '&fields=isbn&fields=authors&fields=title'
fields2 = '&fields=description&fields=publishers&fields=format'
url = url_root + query + fields1 + fields2


def main():
    try:
        book_data = requests.get(url)
        response_data = book_data.json()
        print('Book Data Retrieval Complete')
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error happened: {err}")
    bdata_json = response_data["results"]
    print(bdata_json)
    bookid = 0
    for book_data in bdata_json:
        try:
            if book_data["format"] == "book":
                newbook = Book(id = bookid,
                     isbn = book_data["isbn"],
                     authors = book_data["authors"],
                     title = book_data["title"],
                     description = book_data["description"]
                    )
                print(book["publishers"])
                dbsession.add(newbook)
            else:
                pass
        except KeyError as e:
            print(f'{book["title"]}, {e}')
        dbsession.commit()

if __name__ == "__main__":
    main()
