import os
from flask import Flask, request, jsonify, abort, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

from auth import AuthError, requires_auth

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

from models import Person, Event


'''
PERSONS
'''

@app.route("/persons", methods=['GET'])
@requires_auth('get:requests')
def get_persons(jwt): 

    try:
        persons = Person.query.all()

        return jsonify({
            'success': True,
            'persons': [person.serialize() for person in persons]
        })
    except: 
        abort(404)



@app.route("/persons", methods=['POST'])
@requires_auth('post:requests')
def add_person(jwt):

    body = request.get_json()

    if not ('firstname' in body and 'lastname' in body and 'birthdate' in  body):
        abort(404)

    firstname = body.get('firstname')
    lastname = body.get('lastname')
    birthdate = body.get('birthdate')

    try:
        person = Person(firstname=firstname, lastname=lastname, birthdate=birthdate)
        person.insert()

        return jsonify({
            'success': True
        })

    except:
        abort(422)

@app.route("/persons/<id>", methods=['PATCH'])
@requires_auth('patch:requests')
def update_person(jwt, id):

    person = Person.query.get(id)

    if person: 
        try: 
            body = request.get_json()

            firstname = body.get('firstname')
            lastname = body.get('lastname')
            birthdate = body.get('birthdate')

            if firstname:
                person.firstname = firstname
            if lastname: 
                person.lastname = lastname
            if birthdate: 
                person.birthdate = birthdate
            
            person.update()

            return jsonify({
                'success': True
            })
        except: 
            abort(422)
    else:
        abort(404)

@app.route("/persons/<id>", methods=['DELETE'])
@requires_auth('delete:requests')
def delete_person(jwt, id):

    person = Person.query.get(id)

    if person:
        try:
            person.delete()
            return jsonify({
                'success': True,
                'delete': id
            })
        except:
            abort(422)
    else:
        abort(404)


'''
EVENTS
'''

@app.route("/events", methods=['GET'])
@requires_auth('get:requests')
def get_events(jwt): 

    try:
        events = Event.query.all()

        return jsonify({
            'success': True,
            'events': [event.serialize() for event in events]
        })
    except: 
        abort(404)


@app.route("/events", methods=['POST'])
@requires_auth('post:requests')
def add_event(jwt):

    body = request.get_json()

    if not ('event_type' in body and 'date' in body):
        abort(404)

    event_type = body.get('event_type')
    date = body.get('date')

    try:
        event = Event(event_type=event_type, date=date)
        event.insert()

        return jsonify({
            'success': True
        })

    except:
        abort(422)



# Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": str(error)
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": str(error)
    }), 404

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        'message': ex.error
    }), 401

if __name__ == '__main__':
    app.run()
