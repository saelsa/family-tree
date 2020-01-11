from app import db
import json

class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    birthdate = db.Column(db.String())

    def __init__(self, firstname, lastname, birthdate):
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def insert(self): 
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate,
        }


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(), nullable=False)
    date = db.Column(db.String())



    def __init__(self, event_type, date):
        self.event_type = event_type
        self.date = date
    
    def __repr__(self): 
        return '<id {}>'.format(self.id)

    def insert(self): 
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()
    
    def serialize(self): 
        return {
            'id': self.id,
            'event_type': self.event_type,
            'date': self.date
        }
