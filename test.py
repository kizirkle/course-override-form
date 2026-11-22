import unittest
from website import create_app, models, auth
from flask import get_flashed_messages
from flask_login import login_user

class Test(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # Creating Users

    def testCreateUser(self):
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
    
    # Errors in Creating Users

    def testCreateWrongUser_email_exists(self):
        with self.client as client:
            client.post('/sign-up', data={
                'email': 'glob@gmail.com',
                'firstName': 'glinda',
                'password1': '12345678',
                'password2': '12345678'
            })
            flashes = get_flashed_messages(with_categories=True)
            self.assertEqual(flashes, [('error', 'Email already exists.')])
    
    def testCreateWrongUser_short_email(self):
        with self.client as client:
            client.post('/sign-up', data={
                'email': 'b',
                'firstName': 'glinda',
                'password1': '12345678',
                'password2': '12345678'
            })
            flashes = get_flashed_messages(with_categories=True)
            self.assertEqual(flashes, [('error', 'Email must be greater than 3 characters.')])
    
    def testCreateWrongUser_short_name(self):
        with self.client as client:
            client.post('/sign-up', data={
                'email': 'bl@gmail.com',
                'firstName': 'g',
                'password1': '12345678',                  
                'password2': '12345678'
            })
            flashes = get_flashed_messages(with_categories=True)
            self.assertEqual(flashes, [('error', 'First name must be greater than 2 characters.')])

    def testCreateWrongUser_mismatched_pass(self):
        with self.client as client:
            client.post('/sign-up', data={
                'email': 'bl@gmail.com',
                'firstName': 'glinda',
                'password1': '123458',                  
                'password2': '12345678'
            })
            flashes = get_flashed_messages(with_categories=True)
            self.assertEqual(flashes, [('error', 'Passwords don\'t match.')])

    def testCreateWrongUser_short_pass(self):
        with self.client as client:
            client.post('/sign-up', data={
                'email': 'bl@gmail.com',
                'firstName': 'glinda',
                'password1': '12345',                  
                'password2': '12345'
            })
            flashes = get_flashed_messages(with_categories=True)
            self.assertEqual(flashes, [('error', 'Password must be at least 7 characters.')])

    # Test Login User
    def testLoginUser(self):
        self.testCreateUser()
        with self.client as client:
            login_response = client.post('/login', data={
                            'email': 'glob@gmail.com',
                            'password': '12345678'
                        })
            flashes = get_flashed_messages(with_categories = True)
            self.assertEqual(flashes, [('success', 'Logged in successfully!')])

    # Wrong Logins
    def testWrongLoginUser_incorrect_pass(self):
        self.testCreateUser()
        with self.client as client:
            login_response = client.post('/login', data={
                            'email': 'glob@gmail.com',
                            'password': '12378'
                        })
            flashes = get_flashed_messages(with_categories = True)
            self.assertEqual(flashes, [('error', 'Incorrect password, try again.')])

    def testWrongLoginUser_no_account(self):
        self.testCreateUser()
        with self.client as client:
            login_response = client.post('/login', data={
                            'email': 'gob@gmail.com',
                            'password': '12345678'
                        })
            flashes = get_flashed_messages(with_categories = True)
            self.assertEqual(flashes, [('error', 'Email does not exist.')])

    # Test Submitting Request
    def testHome(self):
        self.app.config['TESTING'] = True
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.testCreateUser()
        self.testLoginUser()
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
    
    # Test Wrong Submitting Request
    def testWrongHome_incomplete_form(self):
        self.app.config['TESTING'] = True
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.testCreateUser()
        self.testLoginUser()
        with self.client as client:
            response = client.post('/', data={
                'student_id': 1,
                'student_name': '',
                'course_name': 'CMSC',
                'course_id': 234,
                'justification': 'I want to take a new class',
            })

            flashes = get_flashed_messages(with_categories=True)
            self.assertEqual(flashes, [('success', 'Logged in successfully!'), ('error', 'All sections of the form must be filled out!')])

if __name__ == '__main__':
    unittest.main()