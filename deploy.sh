#!/bin/sh

# copy project files
scp -r project 130.193.41.149:/home/dimastark/

# connect to backend server
ssh 130.193.41.149

# source all environment variables
set -a
source /home/dimastark/
set +a

# run migrations
python3 /home/dimastark/project/manage.py migrate
python3 /home/dimastark/proejct/manage.py collectstatic --no-input --clear

# restart service
sudo service celery restart
sudo service gunicorn restart
