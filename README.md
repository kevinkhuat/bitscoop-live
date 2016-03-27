BitScoop requires the following installations.

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

Running the BitScoop application during local development requires the following
supporting processes to be active. With the configurations found in `config/`
each of these processes runs without daemonizing and logs to the console.

* `elasticsearch` &ndash; The ElasticSearch server.
* `mongod` &ndash; The MongoDB server.
* `nginx` &ndash; The Nginx reverse proxy.
* `redis-server` &ndash; The Redis server.


## Environment Setup
Create a virtual environment outside the BitScoop repository folder.

Change directory into the bitscoop project folder, activate the virtual
environment and install the requirements with:

```
pip install -r requirements/django.freeze.txt
```

Install the NodeJS requirements with:

```
npm install
```

Edit your host file to point both `bitscoop.com` and `p.bitscoop.com` to
localhost (127.0.0.1). Note this is for development only, if you want to use the
real site, you'll need to comment out this host file entry!


## Initialize ElasticSearch
From the main project directory run:

```
mkdir -p databases/elasticsearch/plugins
```

You can then boot the ElasticSearch server with:

```
elasticsearch --path.conf=config/elasticsearch
```

Before this ElasticSearch database can save data, you must create an index. You
need only do this once, but it must be repeated if you delete the database to
refresh the project. With the ElasticSearch service running:

```
curl -XPUT http://localhost:9200/core
```

This HTTP PUT request should return something along the lines of:

```json
{"acknowledged":true}
```

If you need to refresh the mappings you can recreate the index without deleting
the database by running:

```
curl -XDELETE http://localhost:9200/core
curl -XPUT http://localhost:9200/core
```


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
use bitscoop
db.dummy.insert({})
db.dummy.drop()
exit
```

This will create the `bitscoop` database, write a collection to persist the
database to disk, remove the dummy collection, and exit out of the MongoDB
shell. You should now have a file `databases/mongo/bitscoop.0` if the commands
succeeded (and you ran the commands from the correct folder).


## Initialize Nginx
Nginx is used as a reverse proxy to manage subdomains, SSL, and HTTPS
redirection. While the bitscoop application can technically be accessed directly
over localhost during development, many pages will error out unless you're
hitting the nginx exposed ports (80 or 443).

From the main project directory run:

```
nginx -p . -c config/nginx.conf
```

You'll need to execute this command with sudo privileges to bind to port 80 and
443 (even on localhost).


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

You'll need to insert the initial data into the development sqlite, MongoDB, and
ElasticSearch databases. With your virtual environment active run:

```
python manage.py migrate
python manage.py insert_main_fixtures
python manage.py insert_data
```

Note that if you're working with PostgreSQL you'll need to run

```
python manage.py migrate core
python manage.py migrate
```

When first creating the database. There's an issue with having a custom user table when not using sqlite that
necessitates migrating the user table first. The core app has a user table migration which will address this problem.


## Running a Development Server
You can run a local development server to test changes to the web application.
First make sure you compile the appropriate static files.

```
grunt devel
```

You can watch for file changes and automatically re-run the `devel` Grunt task
with:

```
grunt watch
```

You must also start the main application after activating the virtual
environment from the main project directory with:

```
python manage.py runserver
```


## Quick Reference
Execute these commands from the main project directory to get a development
server up and running. Check the preceeding instructions for more specific
details and examples.

Back-end servers:

```
sudo nginx -p . -c config/nginx.conf
redis-server config/redis.conf
elasticsearch -Des.config=config/elasticsearch/elasticsearch.yml
mongod -f config/mongod.conf
```

Front-end web run from the virtual environment.

```
python manage.py runserver
```
