import datetime
import json
import numpy as np
import os

from flask import Flask, request, jsonify

from models import Book
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']


@app.route("/api/help")
def help():
    help_string = '''
    Welcome to the Oreilly Book API!<br/>
    Available Routes:<br/>
    /<br/>
    /api/help<br/>
    /api/title/<book title><br/>
    /api/bookid/start/end<br/>
    /api/add_book/<br/>
    '''
    return(help_string)


@app.route("/api/title/<title>")
def title_search(title):
    print(title)
    book_ans = db_session.query(Book.id, Book.authors, Book.title,
                                Book.isbn, Book.description).\
                                filter(Book.title.match(f"%{title}%")).all()
    return render_results(book_ans)


@app.route("/api/bookid/<start>/")
@app.route("/api/bookid/<start>/<end>")
def bookid_lookup(start=None, end=None):
    results = []
    if not end:
        book_ans = db_session.query(Book.id, Book.authors, Book.title,
                                    Book.isbn, Book.description).\
                                    filter(Book.id == start).all()
    else:
        book_ans = db_session.query(Book.id, Book.authors, Book.title,
                                    Book.isbn, Book.description).\
                                    filter(Book.id >= start, Book.id <= end).\
                                    all()
    return render_results(book_ans)


@app.route("/api/add_book", methods=['POST'])
def add_book():
    request_data = request.json
    error = dict()
    error["reason"] = ''

    # let's play some defense here:

    if not request_data:
        return error_message_json(error, "needs data")

    content = json.loads(request_data)

    if not content.keys() >= {"bookid", "authors", "isbn",
                              "description", "title"}:
        return error_message_json(error, "please make sure all keys are present
                                  when making api call")

    elif not isinstance(content["bookid"], int):
        return error_message_json(error, "bookid is an int")
    elif not isinstance(content["isbn"], str):
        return error_message_json(error, "isbn is a string of 17 chars in
                                  length")
    elif not isinstance(content["authors"], list):
        return error_message_json(error, "authors is a list of strings.")
    elif not isinstance(content["description"], str):
        return error_message_json(error, "description is a long string.")
    # check following:
    # bookid is there and it's an int
    # isbn is there and it's a string
    # authors is an array of strings
    # title is a string
    # description is a string

    else:
        newbook = Book()
        newbook.id = content["bookid"]
        newbook.isbn = content["isbn"]
        newbook.authors = content["authors"]
        newbook.title = content["title"]
        newbook.description = content["description"]
        db_session.add(newbook)
        db_session.commit()
        success = dict()
        success["reason"] = "book record added"
        results = list(np.ravel(success))
        return jsonify(results=success)


@app.route("/")
def index():
    results = db_session.query(Book.id, Book.authors, Book.title, Book.isbn,
                               Book.description).all()
    return render_results(results)


def render_results(query_res):
    answer = list(np.ravel(query_res))
    return jsonify(results=answer)


def error_message_json(error_dict, error_message):
    error_dict["reason"] = error_message
    prepped_data = list(np.ravel(error_dict))
    return jsonify(results=prepped_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
