import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from models import Person, Event


MEMBER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJEVTRRekE0UkRBMU16a3lNa1ZEUTBJek5UQkRORUV6TUVFME4wUTVNRUUzTkROR1FURXhSZyJ9.eyJpc3MiOiJodHRwczovL3NhZWxzYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUxMGUxZjc3ZGE0NWQwZTk1N2E5NDRiIiwiYXVkIjoiaHR0cHM6Ly9mYW1pbHktdHJlZSIsImlhdCI6MTU3ODc0OTY0MSwiZXhwIjoxNTc4ODM2MDQxLCJhenAiOiJSOWpScXAzNVQxQnFkTmZoZnlOZGFMMjFtZjFrQ0Q1OSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnJlcXVlc3RzIiwiZ2V0OnJlcXVlc3RzIiwicGF0Y2g6cmVxdWVzdHMiLCJwb3N0OnJlcXVlc3RzIl19.K_sVcyENUow63gt1C_aq9pGHXV5yHLfdYYG9E-Ltfdz8mF4zvWG5-MEvLna71IPjx2wXKsrRJRuNcNVcQ8jMzbLs6B1BEtX5y163BGJ7VqZj3EQZmhBeQCs1-IWV9lghPjPBcwRxaUivSmxlYx4lUfZyaSGtZUpshapnKuifpiMgucvnnapY7wTQrAzmI-a4TO7S7IG_2g234sdb2FfimmWLddXWJkcSem1ElnZNgt4k-Yrm6c8g-slamP0wPz0kQLpwuvU-P2WbtZ01ggFGNyHpzZYOLjstMR2NbLp4HUI3B2WBfzcU88J7c8KGySfkFfApJigb9z7FoI3EBil2mg'

class BasicTest(unittest.TestCase):
    def setUp(self):

        app.config.from_object('config.TestingConfig')
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///familytree_test"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json'}

        db.drop_all()
        db.create_all()
 
    # executed after each test
    def tearDown(self):
        pass

    '''
    Persons
    '''

    def test_public_add_person(self):
        new_person = {
            "firstname": "John",
            "lastname": "Doe",
            "birthdate": "01.12.1989"
        }

        res = self.client.post('/persons', json=new_person)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    
    def test_member_add_person(self):
        new_person = {
            "firstname": "John",
            "lastname": "Doe",
            "birthdate": "01.12.1989"
        }
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.post('/persons', json=new_person, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_get_persons(self):
        res = self.client.get('/persons')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_member_get_persons(self):
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.get('/persons', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_update_person(self):
        updated_person = {
            "firstname": "Jane"
        }

        res = self.client.patch('/persons/1', json=updated_person)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_member_update_person(self):
        person = Person(firstname='John', lastname='Doe',
                            birthdate='01.01.1900')
        person.insert()
        person_id = person.id

        updated_person = {
            "firstname": "Jane"
        }

        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.patch(f'/persons/{person_id}', json=updated_person, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_delete_person(self):

        res = self.client.delete('/persons/1', )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_member_delete_person(self):
        person = Person(firstname='John', lastname='Doe',
                            birthdate='01.01.1900')
        person.insert()
        person_id = person.id

        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.delete(f'/persons/{person_id}', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['delete'], str(person_id))

    '''
    EVENTS
    '''
    def test_public_add_event(self):
        new_event = {
            "event_type": "wedding",
            "date": "01.12.1900"
        }

        res = self.client.post('/events', json=new_event)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    
    def test_member_add_event(self):
        new_event = {
            "event_type": "wedding",
            "date": "01.12.1900"
        }
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.post('/events', json=new_event, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_public_get_events(self):
        res = self.client.get('/events')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
    
    def test_member_get_events(self):
        self.headers.update({'Authorization': 'Bearer ' + MEMBER_TOKEN})

        res = self.client.get('/events', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()