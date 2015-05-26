# Contributing to Ografy
This document details the process by which you can set up a development
environment and submit changes to the Ografy core repository.

The general workflow for contributing a change to Ografy is:

1. Fork the repository and clone your fork locally.
2. Suggest an issue or request that an existing, unassigned issue be assigned
   to you.
3. Create an issue branch in your repository to contain your changes.
4. Set up your development environment (if you have not already from previous
   contributions).
5. Develop your changes in your issue branch.
6. Lint and test your changes.
7. Submit a pull request for review. If you have not been assigned to an issue
   and your changes don't solve an open ticket, your pull request will be
   rejected outright.
8. Rebase your changes and/or commit fixes to your proposed pull request if
   requested.


## Set up Git

### Fork the Ografy Repository
You'll want to create a fork of the Ografy repository so that you may freely
create and push to your own branches. Ografy contribution is handled by way of
pull requests to the master repository from your fork. Once you have forked the
repository, clone your fork to your local drive.

### Add an Upstream
You'll want to add the Ografy master repository as an upstream remote. From
within your clone directory, run:

```
git remote add upstream https://github.com/sjberry/ografy.git
```

To track the master repository. To fetch new changes (initially, and
periodically thereafter), run:

```
git fetch upstream
```

To fetch the upstream and clear any removed remote branches from your local
cache, run fetch with the prune flag:

```
git fetch upstream -p
```


## Environment Setup
First you'll need to make sure you've locally installed:

* Python 3.x.x (preferably 3.4.x+) with `pip` and `virtualenv`
* MongoDB
* NodeJS

Since the installation process differs by platform, the details are outside the
scope of this document. Check the official documentation for how to install and
set up these packages.

Create a virtual environment outide the Ografy repository folder, activate it,
 and install the project requirements with:

```
pip install -r requirements/manual.txt
pip install -r requirements/development.txt
```

Install the NodeJS requirements with:

```
npm install
```

Edit your host file to point the following DNS names to localhost (127.0.0.1):

* `mem-0.ografy.internal`
* `nrdb-0.ografy.internal`


### Initialize MongoDB
From the main project directory run:

```
mkdir -p databases/mongo
mongod -f config/mongod.conf
```

Open a new terminal window and connect to the MongoDB service. The run the
following commands:

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


### Initialize Data
You'll want to insert the initial data into the development sqlite and MongoDB databases. With your virtual environment
active (and with the appropriately dependencies installed), run:

```
export DJANGO_SETTINGS_MODULE="ografy.settings.development"
source config/signals.sh
python manage.py migrate
python manage.py insert_main_fixtures
python manage.py insert_data
```

Note that sourcing on API keys found in `config/signals.sh` may fail if the file is not version controlled in the future
with fake keys. You'll need to acquire these keys from an Ografy developer or supply your own.


## Running a Development Server
You can run a local development server to test changes to the web application. First make sure you compile the
appropriate static files.

```
grunt less
grunt nunjucks
```

Then you can start a gunicorn local server from the main project directory with:

```
gunicorn ografy.wsgi --env DJANGO_SETTINGS_MODULE=ografy.settings.development --certfile pki/server.pem --reload
```


## Before Submitting a Pull Request
Before you submit a pull request it is recommended that you run the requisite
linters.

* **flake8** &ndash; Used to enforce the Ografy coding style.
* **isort** &ndash; Used to ensure Python imports are properly sorted.
* **grunt** &ndash; Used to enforce the Ografy coding style for supporting
  static files.

From the root directory run:

```
flake8
isort -rc . --diff
grunt lint
```

If all commands run without any output you're all set. If flake8 or grunt find
any style errors you'll need to fix them manually. If isort finds any style
errors, you can run:

```
isort -rc .
```

To apply the diff displayed earlier. Running the diff command first is not a
prerequisite to actually applying the changes.


### Upstream Master Changed
The master branch on the master repository frequently changes. It is entirely
likely that it will change from the time you create your new branch to the time
your pull request is accepted. This isn't a big deal.

Checkout your local master branch (that presumably tracks upstream/master).

```
git checkout master
```

Rebase against upstream/master, which will advance your master branch's head to
upstream/master branch's head.

```
git rebase upstream/master
```

Push your master branch to your remote ("origin") branch "master".

```
git push origin master
```

Since you shouldn't be making changes directly to your master branch, you should
never ecounter the situation where you need to force push your master branch.

Checkout your issue branch.

```
git checkout issue_xxxx
```

Rebase against upstream/master, which will temporarily undo any commits you've
made, advance your issue branch's head to upstream/master branch's head, and
replay any commits you made on top of the new HEAD.

```
git rebase upstream/master
```

Push your issue branch to your remote issue branch.

```
git push -f origin issue_xxxx
```

In this case the force flag (`-f`) is necessary if you've already pushed
commits to your remote. This is because rebasing off of upstream/master will
modify your git history and you need to forcibly overwrite your remote branch's
history to match your local. This is acceptable because you're working in a
topic branch that people other than your collaborators don't need to reference.


### Modifying a Pull Request
You may be asked to make some changes after opening a pull request. This isn't
difficult. Simply make the changes to your local branch, and push them up to
your remote branch. The pull request will be updated automatically.

If you're asked to squash your commits, this is straightforward as well.
Squashing commits basically means combining the changes you've made in serveral
commits into one (or several) larger commits. You can interactively squash your
commits with a local rebase.

```
git rebase -i HEAD~10
```

In this example you'll combine the changes you've made in the last 10 commits.
`HEAD~10` is merely shorthand for the commit hash 10 commits ago. You can also
type the commit hash explicitly. Usually you'll want to encompass all of your
commits and squash them into a single commit. In any case, once you run that
command, and editor will open summarizing all the commits that have been
selected for squashing. Change "pick" to "squash" for all the commits you'd like
to squash and save the file. Next you'll be prompted to write updated commit
messages in new editor instances. Update your messages as necessary and save.

When you're all done, you'll need to force push to your remote (since you've
just rewritten the history locally).

```
git push -f origin issue_xxxx
```

This should also update your PR automatically.
