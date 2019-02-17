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
