import datetime
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
    find_title_query = Book.query.filter(Book.title.match(f"%{title}%"))
    results = db_session.query(find_title_query)
    return jsonify(render_results(results))

@app.route("/api/bookid/<start>/")
@app.route("/api/bookid/<start>/<end>") 
def bookid_lookup(start=None, end=None):
    if not start:
        results = {}
        return jsonify(results)
    elif not end:
        results = db_session.query(Book).get(start)
        book_dict = {}
        book_dict['id'] = results.id
        book_dict['authors'] = results.authors
        book_dict['title'] = results.title
        book_dict['isbn'] = results.isbn
        book_dict['description'] = results.description
        return jsonify(book_dict)

    else:
        results = db_session.query(Book).filter(Book.id >= start, Book.id <=
                end).all()
        print(results)
        return jsonify(render_results(results))

@app.route("/api/add_book/<bookid>", methods=['POST'])
def add_book(id):
    content = request.json
    newbook = Book(id = bookid,
                   isbn = content["isbn"],
                   authors = content["authors"],
                   title = content["title"],
                   description = content["description"]
                  )
    db_session.add(newbook)
    db_session.commit()

@app.route("/")
def index():
    results = db_session.query(Book.id, Book.authors, Book.title, Book.isbn,
            Book.description).all()

    all_results = []
    for id, authors, title, isbn, description in results:
        book_dict = {}
        book_dict['id'] = id
        book_dict['authors'] = authors
        book_dict['title'] = title
        book_dict['isbn'] = isbn
        book_dict['description'] = description
        all_results.append(book_dict)
    return jsonify(all_results)

def render_results(sql_alchemy_results):
    print(sql_alchemy_results)
    for id, authors, title, isbn, description in sql_alchemy_results:
        book_dict = {}
        book_dict['id'] = id
        book_dict['authors'] = authors
        book_dict['title'] = title
        book_dict['isbn'] = isbn
        book_dict['description'] = description
        all_results.append(book_dict)
    print(all_results)
    return all_results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
