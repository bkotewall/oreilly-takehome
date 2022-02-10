This is a multi container solution to take book data from O'Reilly Media's search api, capture it in a database and build a RESTful api in front to view and insert new data.  

Models.py has the definition of the Book table.  The data_import.py script
populates the table.

Database.py defines the uri and the database handle for the database and will 
be referenced throughout this code.

App.py is a flask app that provides the RESTful interface as specified in the
code specifications.  

(Need to write more docs...)

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
