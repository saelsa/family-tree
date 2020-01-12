import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app, db
from models import Person, Event


MEMBER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJEVTRRekE0UkRBMU16a3lNa1ZEUTBJek5UQkRORUV6TUVFME4wUTVNRUUzTkROR1FURXhSZyJ9.eyJpc3MiOiJodHRwczovL3NhZWxzYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUxMGUxZjc3ZGE0NWQwZTk1N2E5NDRiIiwiYXVkIjpbImh0dHBzOi8vZmFtaWx5LXRyZWUiLCJodHRwczovL3NhZWxzYS5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc4ODU5ODgyLCJleHAiOjE1Nzg5NDYyODIsImF6cCI6IlI5alJxcDM1VDFCcWROZmhmeU5kYUwyMW1mMWtDRDU5Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpyZXF1ZXN0cyIsImdldDpyZXF1ZXN0cyIsInBhdGNoOnJlcXVlc3RzIiwicG9zdDpyZXF1ZXN0cyJdfQ.DKfVaYnCut36p9SNNE3AuLl1-7RTO7h_YcgaqgiGSnNl2263iZ2TH3tLllXdOWfsM1bckOf-2BBklbX9r-SO6E-0WzXwIyHVwRDc7l7_ihkA_lr8oKzPox1a9rwAvGbwk28hxWFjmCOavDzVpUh0P0gY84A8K0DcN1GcvVmOyklQhz4H8wNVU1c_WtRRk7RpXLbUtPMSYBSUqZbISzGmPYhAC0OuhVO3w_Iman7GSMnhlgfAIY0XU2DxVMIydPi_STGSp2SQCmLi7wOrZIM2KKFfD54a35lKPZvNM1u2dg3egk0qlvGy9kKvG5Jm2EK06vabJEOQH-CkyK9tdNFobQ'

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