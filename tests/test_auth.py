from tests.test import BaseTest
import json


class TestAuthentication(BaseTest):
    def test_successful_registration(self):
        userdata = {'username': 'judith', 'password': 'flaskapi'}
        response = self.client.post('/auth/register',
                                    data=json.dumps(userdata),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_unsuccessful_registration(self):
        # register with existing username
        userdata = {'username': 'user1', 'password': 'testpass'}
        response = self.client.post('/auth/register',
                                    data=json.dumps(userdata),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.get_data(as_text=True))
        self.assertIn('User already exists!', message['message'])

    def test_register_without_password(self):
        # register without password
        userdata = {'username': 'user1'}
        response = self.client.post('/auth/register',
                                    data=json.dumps(userdata),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.get_data(as_text=True))
        self.assertIn('Please enter username and password', message['message'])

    def test_register_without_password_and_username(self):
        # register without username and passsword
        userdata = {}
        response = self.client.post('/auth/register',
                                    data=json.dumps(userdata),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.get_data(as_text=True))
        self.assertIn('Please enter username and password', message['message'])

    def test_successful_login(self):

        userdata = {'username': 'user1', 'password': 'password1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_blank_login(self):
        # blank login
        userdata = {}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_bad_credentials_login(self):
        # login with bad credentials
        userdata = {'username': 'user1', 'password': 'password2'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_login_without_password(self):
        # login without password
        userdata = {'username': 'user1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_login_without_username(self):
        # login without username
        userdata = {'password': 'password1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_login_with_nonexisting_username(self):
        # non existing username
        userdata = {'username': 'user4', 'password': 'password1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 400)
