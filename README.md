# django-base
A basic boilerplate Django project prepped with poetry and Rollup. It uses the Django project default database SQLite.

## Setup

For history's sake, this setup was based off of the instructions here: https://builtwithdjango.com/blog/basic-django-setup.

1. Install [poetry](https://python-poetry.org/docs/#installation). This allows us to run our project in a virtual environment and will handle the installation of Django and other python libraries.

2. Run `poetry install` to install dependencies.

3. Rename `swiftproject` to whatever you'd like your project to be named. You will want to change the name in `pyproject.toml`, the Django project directory name `swiftproject/`, `manage.py`, and `settings.py`.

4. Change `TIME_ZONE` in `settings.py` to your timezone.

5. Run `poetry run python manage.py migrate` to initialize your local database.

6. Create a superuser for your local Django instance. Run `poetry run python manage.py createsuperuser`. Be sure to save your username and password in a responsible location.

7. Install [node](https://nodejs.org/en).

8. Run `npm install`.

9. Run `npm run build`.

## Running the server

Run `poetry run python manage.py runserver`.


## Running other Django commands

See Django documentation for other commands, such as generating and applying migrations. Commands can be used as normal, preceded by `poetry run`. For example, see "Running the server" above.

## Running tests

To run python tests, use `poetry run pytest`.
To run TS/JS tests, use `npm run test`.

## Additional information

In this project we read the research data from events_data.csv file, located in the root directory django-base-main 

The column names in events_data.csv file:

Event date
Event name
Event description
Tags
Link to additional info 

Tags are some helpful identifying tags for the type of event in question.
Our goal is to find the corellation between the events in research and the updates on the relevant Wiki pages.
We'll create a dashboard to illustrate the corellation.

## VSCode Project setup

The project is implemented in VSCode IDE

1. In the VSCode terminal, in the root directory (django-base-main), create virtual environment using command:
python -m venv venv

activate virtual environment using command: 
.\venv\Scripts\activate

2. Execute the steps 1-7 to install the dependencies and build the project.
install some additional dependencies:

pip install plotly
pip install pandas
pip install requests
pip install wikipedia
pip install colorhash


3. In the virtual environment, execute custom command to create objects for the events and populate the database:

(venv) PS C:\Users\...\django-base-main>python manage.py load_events

4. The server is run with the command:

python manage.py runserver

5. Access the chart with url:

http://127.0.0.1:8000/


## Project components

## Project Models

In this app, two models are implemented in 
dashboard\models.py

- Event is a model created for the objects based on the data from events_data.csv 
- WikiRevisionEvent is a model created for the data retrieved from Wiki, using Wiki revisions API:

https://www.mediawiki.org/wiki/API:Revisions 

## Project Custom command 'load_events'

Custom command is implemented in :
dashboard\management\commands\load_events.py


The command creates 2 types of objects based on 2 models and 
populates the database sqlite with the data from events_data.csv file and Wiki revisions 

## View (the dashboard)

The dashboard component is implemented in :
dashboard\views.py

Plotly framework is used for the dashboard.

The view is created with 2 graph_objects, populated with wiki_data and data from events_data.csv file for comparisson

The data is derived from tags obtained from a CSV document 
and Wikipedia revisions of the event date plus the subsequent six months.
Additionally, the Wiki events have been grouped by month periods.

After we start the server, we can access the chart with url:

http://127.0.0.1:8000/











