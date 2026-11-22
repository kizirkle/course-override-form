import unittest
from website import create_app, models, auth
from flask import get_flashed_messages
from flask_login import login_user

class Test(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def createUser(self):
        with self.client as client:
            response = client.post('/sign-up', data={
                'email': 'glob@gmail.com',
                'firstName': 'glob',
                'password1': '12345678',
                'password2': '12345678'
            })
            flashes = get_flashed_messages(with_categories=True)
            if not models.User.query.filter_by(email='glob@.gmail.com').first():
                self.assertEqual(flashes, [('error', 'Email already exists.')])
            else:
                self.assertEqual(flashes, (['Account created!', 'success']))

    def loginUser(self):
        self.createUser()
        with self.client as client:
            login_response = client.post('/login', data={
                            'email': 'glob@gmail.com',
                            'password': '12345678'
                        })
            flashes = get_flashed_messages(with_categories = True)
            self.assertEqual(flashes, [('success', 'Logged in successfully!')])

    def testHome(self):
        self.app.config['TESTING'] = True
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.createUser()
        self.loginUser()
        with self.client as client:
            response = client.post('/', data={
                'student_id': 1,
                'student_name': 'eve',
                'course_name': 'CMSC',
                'course_id': 234,
                'justification': 'I want to take a new class',
            })

            flashes = get_flashed_messages(with_categories=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(flashes, [('success', 'Logged in successfully!'), ('success', 'Request submitted!')])

if __name__ == '__main__':
    unittest.main()