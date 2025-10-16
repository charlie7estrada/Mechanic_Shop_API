from app import create_app
from app.models import Mechanic, ServiceTickets, db
from werkzeug.security import check_password_hash, generate_password_hash
import unittest
from app.utils.util import encode_token

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(
            name="tester",
            email="tester@email.com",
            phone="123-456-7890",
            salary=40000,
            password="123"
        )  
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            self.mechanic_id = self.mechanic.id  
        self.token = encode_token(self.mechanic_id)  # encoding a token for starter mechanic
        self.client = self.app.test_client()

    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "test_mechanic",
            "email": "test@email.com",
            "phone": "111-222-3333",
            "salary": 50000,
            "password": "123"
        }

        response = self.client.post("/mechanics", json=mechanic_payload)
        print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['email'], 'test@email.com')

    def test_invalid_mechanic(self):
        mechanic_payload = {  # Missing email field
            "name": "Bad Mechanic",
            "phone": "111-222-3333",
            "salary": 50000,
            "password": "123"
        }

        response = self.client.post("/mechanics", json=mechanic_payload)
        self.assertIn("email", response.json)
        self.assertIn("Missing data for required field.", response.json["email"])

    def test_login(self):
        login_creds = {
            "email": "tester@email.com",
            "password": "123"
        }

        response = self.client.post('/mechanics/login', json=login_creds)
        self.assertEqual(response.status_code, 200)
        self.assertIn('auth_token', response.json)

    def test_get_mechanics(self):
        response = self.client.get('/mechanics')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['email'], 'tester@email.com')

    def test_non_unique_email(self):
        mechanic_payload = {
            "name": "Dup Mechanic",
            "email": "tester@email.com",  # duplicate email
            "phone": "999-888-7777",
            "salary": 45000,
            "password": "123"
        }

        response = self.client.post('/mechanics', json=mechanic_payload)
        self.assertNotEqual(response.status_code, 201)
        self.assertIn('email', response.get_data(as_text=True).lower())

    def test_delete(self):
        headers = {'Authorization': "Bearer " + self.token}

        response = self.client.delete(f'/mechanics/{self.mechanic_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully deleted', response.json['message'])

    def test_unauthorized_delete(self):
        response = self.client.delete(f'/mechanics/{self.mechanic.id}')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token', response.json['message'])

    def test_update(self):
        headers = {"Authorization": "Bearer " + self.token}

        update_payload = {
            "name": "Updated Tester",
            "email": "updated@email.com",
            "phone": "555-555-5555",
            "salary": 60000,
            "password": "456"
        }

        response = self.client.put(f'/mechanics/{self.mechanic.id}', headers=headers, json=update_payload)
        print(response.json)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'updated@email.com')

    def test_my_tickets_no_mechanic(self):
        headers = {"Authorization": "Bearer " + self.token}

        response = self.client.get('/mechanics/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'Mechanic not found')

    

if __name__ == "__main__":
    unittest.main()