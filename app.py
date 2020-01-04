import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import Person

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/add")
def add_person():
    firstname=request.args.get('firstname')
    lastname=request.args.get('lastname')
    try: 
        person=Person(firstname=firstname, lastname=lastname)
        db.session.add(person)
        db.session.commit()
        return "Person added. book id={}".format(person.id)
    except Exception as e: 
        return(str(e))

@app.route("/getall")
def get_all():
    try:
        persons=Person.query.all()
        return jsonify([e.serialize() for e in persons])
    except Exception as e: 
        return(str(e))

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        person=Person.query.filter_by(id=id).first()
        return jsonify(person.serialize())
    except Exception as e: 
        return(str(e))




if __name__ == '__main__':
    app.run()
