import unittest
from api import db, create_app
from api.models import User, Bucketlist, Item
import json


class BaseTest(unittest.TestCase):

    def setUp(self):
        app = create_app('testing')
        self.context = app.app_context()
        self.context.push()
        db.create_all()
        self.client = app.test_client()

        user1 = User(username='user1', password='password1')
        bucketlist1 = Bucketlist(name='Do crazy things')
        bucketlist1.user = user1

        item1 = Item(
            name="Bungee jumping",
            done='False',
            bucketlist_id=1
        )
        # item1.bucketlist = bucketlist1
        item2 = Item(
            name="Zip lining",
            done='True',
            bucketlist_id=1
        )
        # item2.bucketlist = bucketlist1
        db.session.add_all([user1, bucketlist1, item1, item2, ])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def retrieve_token(self):
        response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'username': 'user1',
                'password': 'password1',
            }),
            content_type='application/json',
        )
        token = json.loads(response.get_data(as_text=True)).get('token')
        return token
