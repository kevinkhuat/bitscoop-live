Ografy requires the following installations.

* ElasticSearch 
* MongoDB
* Nginx
* NodeJS
* PostgreSQL
* Python 3.x.x (preferably 3.4.x+) with `pip` and `virtualenv`
* Redis

Since the installation process differs by platform, the details are outside the
scope of this document. Check the official documentation for how to install and
set up these packages.

Running the Ografy application during local development requires the following
supporting processes to be active. With the configurations found in `config/`
each of these processes runs without daemonizing and logs to the console.

* `elasticsearch` &ndash; The ElasticSearch server.
* `mongod` &ndash; The MongoDB server.
* `nginx` &ndash; The Nginx reverse proxy.
* `redis-server` &ndash; The Redis server.


## Environment Setup
Create a two virtual environments outide the Ografy repository folder. You'll
need one for the Django app and one for the Tornado app since the dependencies
conflict.

Change directory into the ografy project folder, activate the Django virtual
environment and install the requirements with:

```
pip install -r requirements/django.txt
pip install -r requirements/development.txt
```

In a separate terminal activate the Tornado virtual environment and install the
requirements with:

```
pip install -r requirments/tornado.txt
pip install -r requirments/development.txt
```

Install the NodeJS requirements with:

```
npm install
```

Edit your host file to point `ografy.io` to localhost (127.0.0.1). Note this is
for development only, if you want to use the real site, you'll need to comment
out this host file entry!


## Initialize ElasticSearch
From the main project directory run:

```
mkdir -p databases/elasticsearch/plugins
```

You can then boot the ElasticSearch server with:

```
elasticsearch -Des.config=config/elasticsearch/elasticsearch.yml
```

Before you run the application you'll need to create the appropriate indices in
the database. With the ElasticSearch server running:

```
curl -XPUT http://localhost:9200/core
```

This HTTP PUT request should return something along the lines of:

```json
{"acknowledged":true}
```

#### A note about ElasticSearch mappings:
ElasticSearch field mappings are PUT into the database when `run_tornado.py` is
run. On a freshly-created index, the mapping is created and applied. If a
mapping already exists, ElasticSearch will attempt to merge the old and new
mapping; if they're identical, then nothing new will happen and the mappings
will remain the same. Restarting the Tornado server should have no effect on
existing mappings since the mappings it attempts to apply should be identical to
what is already there.

In production, it should be impossible to insert data into ElasticSearch without
a mapping present since the act of starting the Tornado server performs the
mappings, and the Tornado server is the only place where data is inserted into
ElasticSearch. If you are manually inserting data into ElasticSearch in
development, such as by running the `insert_data` command, it is possible to
insert data when no mapping exists. If you encounter ElasticSearch mapping
errors, first delete the existing ElasticSearch index by running:

```
curl -XDELETE http://localhost:9200/core
```

Then re-create the index with:

```
curl -XPUT http://localhost:9200/core
```

Restart the Tornado server to have it insert the field mappings, and then
finally add the manual data you were attempting to before.


## Initialize MongoDB
From the main project directory run:

```
mkdir -p databases/mongo
```

You can then boot the MongoDB server with:

```
mongod -f config/mongod.conf
```

Before this MongoDB server can save data, the appropriate database must be
initialized. You need only do this once, but it must be repeated if you delete
the database to refresh the project. Open a new terminal window and connect to
the MongoDB service. The run the following commands in the MongoDB command line:

```
use ografy_db
db.dummy.insert({'test':'data'})
db.getCollection('dummy').drop()
exit
```

This will create the `ografy_db` database, write a collection to persist the
database to disk, remove the dummy collection, and exit out of the MongoDB
shell. You should now have a file `databases/mongo/ografy_db.0` if the commands
succeeded (and you ran the commands from the correct folder).


## Initialize Nginx
Nginx is used as a reverse proxy to manage subdomains, SSL, and HTTPS
redirection. While the ografy application can technically be accessed directly
over localhost during development, many pages will error out unless you're
hitting the nginx exposed ports (80 or 443).

From the main project directory run:

```
nginx -p . -c config/nginx.conf
```

You'll need to execute this command with sudo privileges to bind to port 80 and
443 (even on localhost). You can change the ports in the configuration if you
need to, but the application is not tested against this.


## Initialize Redis
From the main project directory run:

```
mkdir -p databases/redis
```

You can then boot the Redis server with:

```
redis-server config/redis.conf
```


## Insert Initial Data

You'll need to insert the initial data into the development sqlite and MongoDB
databases. With your virtual environment active run:

```
export DJANGO_SETTINGS_MODULE="ografy.settings.development"
source config/signals.sh
python manage.py migrate
python manage.py insert_main_fixtures
python manage.py insert_data
```

The MongoDB server needs to be available for the `insert_main_fixtures` and
`insert_data` management commands to succeed.

Note that sourcing on API keys found in `config/signals.sh` may fail if the file
is not version controlled in the future with fake keys. You'll need to acquire
these keys from an Ografy developer or supply your own.


## Running a Development Server
You can run a local development server to test changes to the web application.
First make sure you compile the appropriate static files.

```
grunt less
grunt nunjucks
```

You need to start the tornado auth server after activating the Tornado virtual
environment from the main project directory with:

```
python tornado.py
```

You must also start the main application after activating the Django virtual
environment from the main project directory with:

```
gunicorn wsgi --env DJANGO_SETTINGS_MODULE=ografy.settings.development --reload
```
