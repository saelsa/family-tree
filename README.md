# Full Stack Familytree API Backend

## About

The project provides the backbone to create and visualize a family tree. Members can manage information about family members and their ancestors as well as important family events. Guests can retrieve that information. At a future stage, persons and events will be linked in order to create a family tree.

https://fsnd-family-tree.herokuapp.com

## API

In order to use the API users need to be authenticated. Users can either have a guest or a member status. An overview of the API can be found below as well as in the provided postman collection.

### Retreiving data (Guests and members)

**GET** `/persons`

Retrieves a list of family members

```
curl -X GET \
  https://fsnd-family-tree.herokuapp.com/persons \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

**GET** `/events`

Retrieves a list of events

```
curl -X GET \
  https://fsnd-family-tree.herokuapp.com/events \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>'
```

### Managing data (Members only)

**POST** `/persons`

Add a new person

```
curl -X POST \
  https://fsnd-family-tree.herokuapp.com/persons \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname": "John",
    "lastname": "Doe",
    "birthdate": "01.01.2000"
}'
```

**PATCH** `/persons/<id>`

Change information for a given person

```
curl -X PATCH \
  https://fsnd-family-tree.herokuapp.com/persons/1 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname": "Jane"
}'
```

**DELETE** `/persons/<id>`

Delete a given person

```
curl -X DELETE \
  https://fsnd-family-tree.herokuapp.com/persons/5 \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN> ' \

```

**POST** `/events`

Add a new event

```
curl -X POST \
  https://fsnd-family-tree.herokuapp.com/persons \
  -H 'Authorization: Bearer <INSERT_YOUR_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '{
    "event_type": "wedding",
    "date": "01.01.2020"
}'
```

## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

The project requires Python 3.6. Using a virtual environment such as `pipenv` is recommended. Set up the project as follows:

```

pipenv shell
pipenv install

```

### Database Setup

With Postgres running, create a database:

```

sudo -u postgres createdb familytree

```

### Running the server

To run the server, first set the environment variables, then execute:

```bash
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL="postgresql:///familytree"
python manage.py runserver
```

## Testing

To test the API, first create a test database in postgres and then execute the tests as follows:

```
sudo -u postgres createdb familytree_test
python test_app.py
```
