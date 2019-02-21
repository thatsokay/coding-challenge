# Coding Challenge

Submit URLs to be tested.

## Requirements

- Python 3.6
- Virtualenv
- RabbitMQ

## Installation

Create a virtual environment to install the Python dependencies.

```bash
# Create and activate virtualenv
virtualenv venv -p python3
. venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set Django secret key
export SECRET_KEY=<secret key>
```

### To run Django's test server

```bash
export DEBUG=true
python manage.py runserver
```

### To deploy to a production server

1. Create Gunicorn systemd service file at `/etc/systemd/system/gunicorn.service`
1. Start Gunicorn service with `systemctl start gunicorn`
1. Install Nginx
1. Create Nginx config file at `/etc/nginx/sites-available/<project name>`
1. Link config to enabled sites with `ln -s /etc/nginx/sites-available/<project name> /etc/nginx/sites-enabled`
1. Restart Nginx with `systemctl restart nginx`
1. Create Celery config file at `/etc/conf.d/celery`
1. Create Celery systemd service file at `/etc/systemd/system/celery.service`
1. Start Celery service with `systemctl start gunicorn`

Sample configuration files can be found below.

## Testing

`python manage.py test`

Ensure that the virtual environment is activated and secret key is set.

## Architecture

### Frontend

The frontend shows an input field for submitting jobs and a table displaying
completed jobs. It uses Vue.js to submit jobs to, and update its job history
from the API server. Runs on the same server as the API.

### API Server

The API server provides two endpoints: `add_job` and `get_jobs`.

`add_job` adds a task to a RabbitMQ message queue. A Celery worker can take a
task from the message queue and execute it, adding the result to Django's
database.

`get_jobs` queries the database and returns a list of completed jobs.

The server runs as a Django application on an AWS EC2 instance.

### Data Persistence Layer

A PostgreSQL database on AWS RDS is used for storing the job results.

### Job Runner

Celery is a distributed task queue that manages workers processes. The
number of workers can be configured through Celery's config file. Celery
relies on a message broker (such as RabbitMQ) to distribute messages
between workers.

## Project Structure

- `api/` is the Django app for the API server.
  - `api/tasks.py` defines the Celery tasks.
  - `api/tests.py` defines the API tests.
  - `api/views.py` defines the API endpoints.
- `challenge/` contains configuration files for Django and Celery.
- `frontend/` is the Django app for the frontend.
  - `frontend/static/frontend/index.js` contains the Vue.js application running on the frontend.
  - `frontend/static/frontend/index.css` contains the styling on the frontend.
  - `frontend/templates/frontend/index.html` is the template used to render the frontend page.

## Sample Configurations

Start and enable services after creating systemd service files.

```
systemctl start <service name>
systemctl enable <service name>
```

### Gunicorn

#### `/etc/systemd/system/gunicorn.service`

```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=<username>
Group=www-data
WorkingDirectory=<project directory>
ExecStart=<project directory>/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:<project directory>/<project name>.sock <project name>.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Nginx

#### `/etc/nginx/sites-available/<project name>`

```
server {
    listen 80;
    server_name <server domain or IP>;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root <project directory>;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:<project directory>/<project name>.sock;
    }
}
```

### Celery

#### `/etc/conf.d/celery`

```
# Names of nodes to start
#   most people will only start one node:
CELERYD_NODES="worker1"
#   but you can also start multiple and configure settings
#   for each in CELERYD_OPTS
#CELERYD_NODES="worker1 worker2 worker3"
#   alternatively, you can specify the number of nodes to start:
#CELERYD_NODES=10

# Absolute or relative path to the 'celery' command:
#CELERY_BIN="/usr/local/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"
CELERY_BIN="<project directory>/venv/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="<project name>"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

# Where to chdir at start.
#CELERYD_CHDIR="/opt/Myproject/"
CELERYD_CHDIR="<project directory>"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=8"
# Configure node-specific settings by appending node name to arguments:
#CELERYD_OPTS="--time-limit=300 -c 8 -c:worker2 4 -c:worker3 2 -Ofair:worker1"

# Set logging level to DEBUG
#CELERYD_LOG_LEVEL="DEBUG"
CELERYD_LOG_LEVEL="INFO"

# %n will be replaced with the first part of the nodename.
#CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
#CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="<project directory>/%n%I.log"
CELERYD_PID_FILE="<project directory>/%n.pid"

# Workers should run as an unprivileged user.
#   You need to create this user manually (or you can choose
#   a user/group combination that already exists (e.g., nobody).
CELERYD_USER="celery"
CELERYD_GROUP="celery"

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1

# How to call manage.py
CELERYD_MULTI="multi"
```

#### `/etc/systemd/system/celery.service`

```
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=<project directory>
ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'

[Install]
WantedBy=multi-user.target
```
