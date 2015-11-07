# Contributing to BitScoop
This document details the process by which you can set up a development
environment and submit changes to the BitScoop core repository.

The general workflow for contributing a change to BitScoop is:

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

### Fork the BitScoop Repository
You'll want to create a fork of the BitScoop repository so that you may freely
create and push to your own branches. BitScoop contribution is handled by way of
pull requests to the master repository from your fork. Once you have forked the
repository, clone your fork to your local drive.

### Add an Upstream
You'll want to add the BitScoop master repository as an upstream remote. From
within your clone directory, run:

```
git remote add upstream https://github.com/bitscooplabs/web-server.git
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


## Before Submitting a Pull Request
Before you submit a pull request it is required that you run the requisite
linters.

* **flake8** &ndash; Used to enforce the BitScoop coding style.
* **isort** &ndash; Used to ensure Python imports are properly sorted.
* **grunt** &ndash; Used to enforce the BitScoop coding style for supporting
  static files.

Activate the bitscoop virtual environment (or a new virtual environment
specifically for testing) and install the development dependencies:

```
pip install -r requirements/development.txt
npm install
```

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
