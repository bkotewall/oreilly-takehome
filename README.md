This is a multi container solution to take book data from O'Reilly Media's search api, capture it in a database and build a RESTful api in front to view and insert new data.  

Models.py has the definition of the Book table.  The data_import.py script
populates the table.

Database.py defines the uri and the database handle for the database and will 
be referenced throughout this code.

App.py is a flask app that provides the RESTful interface as specified in the
code specifications.  

Available Routes:<br/>
    /
    This returns all books in the database in json form.

    /api/help
    This provides a rudimentary list of all defined routes.

    /api/title/<book title>
    Select book(s) by title e.g. GET /api/title/"somestr"
    This would return a json array with book titles that include "somestr"
    
    /api/bookid/start
    Select book by bookid e.g. GET /api/bookid/12.   
    This would return a json array with one dictionary of book 12.
    
    /api/bookid/start/end
    Select book by range of bookids e.g. GET /api/bookid/12/18
    This would return a json array with dictionaries of books 12 to 18,
    inclusive.

    /api/add_book/
    Please refer to test_post.py as how to send data to the api.


## Usage

1. Bootstrap the DB
```bash
$ docker-compose up -d db
$ docker-compose run --rm flaskapp /bin/bash -c "cd /opt/services/flaskapp/src && python -c  'import database; database.init_db()' && python -c 'import data_import; data_import.import_data()' "
```

2. Bring up the cluster
```bash
$ docker-compose up -d
```

3. Browse to localhost:8080 to see the app in action.
