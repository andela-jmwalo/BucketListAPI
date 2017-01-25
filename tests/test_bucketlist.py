from tests.test import BaseTest
import json


class TestBucketList(BaseTest):
    def test_add_bucketlist(self):
        bucketlist2 = {'name': 'Visit new cities'}
        response = self.client.post(
            '/bucketlists/',
            data=json.dumps(bucketlist2), headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        self.assertIn(message, 'Bucketlist created successfully')

    def test_add_bucketlist_without_name(self):
        bucketlist3 = {}
        response = self.client.post(
            '/bucketlists/',
            data=json.dumps(bucketlist3), headers=self.get_token())
        self.assertEqual(response.status_code, 400)

    def get_bucketlists(self):

        response = self.client.get(
            '/bucketlists/', headers=self.get_token)
        self.assertEqual(response.status_code, 200)

    def get_bucketlist_with_id(self):
        response = self.client.get(
            '/bucketlists/1', headers=self.get_token)
        self.assertEqual(response.status_code, 200)
        bucketlist2 = json.loads(response.data)
        self.assertEqual(bucketlist2.get('name'), 'Do crazy things')

    def test_get_bucketlist_with_nonexistent_id(self):

        response = self.client.get("/bucketlists/50",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 403)
        #204 or 404
        output = json.loads(response.data)
        self.assertEqual(output['message'], 'Bucketlist does not exist')

    def update_bucketlist(self):
        bucketlist2 = {'name': 'Go to new towns'}
        response = self.client.put("/bucketlists/1",
                                data=self.bucketlist2,
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertIn(output['message'],
                      'Bucketlist updated successfully')
        self.assertEqual(bucketlist2.get['name'], 'Go to new towns')

    def delete_bucketlist(self):
        response = self.client.delete("/bucketlists/1",
                                   data=self.bucketlist1,
                                   headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        #check if the resource wa deleted check 204
        output = json.loads(response.data)
        self.assertIn(output['message'],
                      'Bucketlist deleted successfully')

    #test user accessing other users resources
    #test search with name 
