from tests.test import BaseTest
import json


class TestBucketList(BaseTest):

    def test_add_bucketlist(self):
        bucketlist2 = {'name': 'Travel', 'description': 'Visit new cities'}
        response = self.client.post(
            '/bucketlists/',
            data=json.dumps(bucketlist2),
            headers={"Authorization": self.retrieve_token(),
                     'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.get_data(as_text=True))
        self.assertIn('Bucketlist created successfully', message['message'])

    def test_add_blank_bucketlist(self):
        bucketlist3 = {}
        response = self.client.post(
            '/bucketlists/',
            data=json.dumps(bucketlist3),
            headers={"Authorization": self.retrieve_token(),
                     'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_get_bucketlists(self):

        response = self.client.get(
            '/bucketlists/', headers={"Authorization":
                                      self.retrieve_token(),
                                      'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlist_with_id(self):
        response = self.client.get(
            '/bucketlists/1', headers={"Authorization":
                                       self.retrieve_token(),
                                       'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        bucketlist2 = json.loads(response.get_data(as_text=True))
        self.assertEqual(bucketlist2.get('name'), 'Do crazy things')

    def test_get_bucketlist_with_nonexistent_id(self):

        response = self.client.get(
            '/bucketlists/500', headers={"Authorization":
                                         self.retrieve_token(),
                                         'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_update_bucketlist(self):
        bucketlist1 = {'name': 'Go to new towns',
                       'description': 'Visit new towns'}
        response = self.client.put(
            '/bucketlists/1', data=json.dumps(bucketlist1),
            headers={"Authorization": self.retrieve_token(),
                     'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        response = self.client.delete(
            '/bucketlists/1', headers={"Authorization":
                                       self.retrieve_token(),
                                       'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
