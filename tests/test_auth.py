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
        message = json.loads(response.data)
        self.assertIn('username already exists', message)

        # register without password
        userdata = {'username': 'user1'}
        response = self.client.post('/auth/register',
                                 data=json.dumps(userdata),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        self.assertIn('No registration without password', message)
        #register without username and passsword
        userdata = {}
        response = self.client.post('/auth/register',
                                 data=json.dumps(userdata),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        message = json.loads(response.data)
        

    def test_successful_login(self):
    
        userdata = {'username': 'user1', 'password': 'password1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_login(self):
        # blank login
        userdata = {}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)
        # login with bad credentials
        userdata = {'username': 'user1', 'password': 'password2'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)
        # login without password
        userdata = {'username': 'user1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)
        # login without username
        userdata = {'password': 'password1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)
        # non existing username
        userdata = {'username': 'user4', 'password': 'password1'}
        response = self.client.post(
            '/auth/login', data=json.dumps(userdata),
            content_type='application/json')

        self.assertEqual(response.status_code, 401)
    
