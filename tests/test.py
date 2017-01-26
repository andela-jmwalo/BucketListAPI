import unittest
from api import db, create_app
from api.models import User, Bucketlist, Item


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
        )
        item1.bucketlist = bucketlist1
        item2 = Item(
            name="Zip lining",
            done='True',

        )
        item2.bucketlist = bucketlist1
        db.session.add_all([user1, bucketlist1, item1, item2, ])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
