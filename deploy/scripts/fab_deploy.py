import fabtools
from contextlib import contextmanager as _contextmanager
from fabric.api import *
from fabtools import require

env.directory = '.'
env.activate = 'source /envs/fab/bin/activate'

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

@task
def setup():
    with virtualenv():

        # Require a PostgreSQL server
        #ToDo Move this to other deployment script to be used on PostgreSQL server box
        require.postgres.server()
        require.postgres.user('myuser', 's3cr3tp4ssw0rd')
        require.postgres.database('myappsdb', 'myuser')

        # Require a supervisor process for our app
        require.supervisor.process('myapp',
            command='/home/myuser/env/bin/gunicorn_paster /home/myuser/env/myapp/production.ini',
            directory='/home/myuser/env/myapp',
            user='myuser'
            )

        # Require an nginx server proxying to our app
        require.nginx.proxied_site('example.com',
            docroot='/home/myuser/env/myapp/myapp/public',
            proxy_url='http://127.0.0.1:8888'
            )
        with cd('ografy/ografy'):
            run('pip install -r requirements.txt')
            run('manage.py syncdb')
            run('manage.py validate')
            #Do some South-based database upgrade nonsense
            #Set some connector arguments to hook up to PostgreSQL server
            #Todo Figure out how to break apart serving of static files and the web server
            #Todo Start Phusion process
    yield