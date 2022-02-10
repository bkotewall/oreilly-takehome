import datetime
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
    content = request.json
    if not content:
        error = dict()
        error["reason"] = "please pass the right argument"
        results = list(np.ravel(error))
        return jsonify(results=error)
    else:
        print(content)
        newbook = Book(id=content["bookid"],
                       isbn=content["isbn"],
                       authors=content["authors"],
                       title=content["title"],
                    description=content["description"])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
