#!/bin/bash

cd /home/ketocalc/ketocalc

# ensure to get origin's data and discard any local change
git fetch
git reset origin/master --hard
git pull

# install packages
pipenv install

# upgrade database
pipenv run flask db upgrade