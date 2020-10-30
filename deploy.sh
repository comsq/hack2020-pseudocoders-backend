#!/bin/sh

# copy project files
scp -r project 130.193.41.149:/home/dimastark/

# connect to backend server
ssh dimastark@130.193.41.149 '
cd /home/dimastark/

# source all environment variables
set -a
source backend-env
set +a

# configure environment
cd project

/home/dimastark/.local/bin/pipenv install --deploy --system --ignore-pipfile
python3 /home/dimastark/project/manage.py migrate
python3 /home/dimastark/project/manage.py collectstatic --no-input --clear

# restart service
sudo service celery restart
sudo service gunicorn restart
'
