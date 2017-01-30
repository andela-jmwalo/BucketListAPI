from tests.test import BaseTest
import json


class TestItem(BaseTest):
    def test_add_item(self):
        item3 = {'name': 'Zip Lining'}
        response = self.client.post(
            '/bucketlists/1/items/',
            data=json.dumps(item3),
            headers={"Authorization": self.retrieve_token(),
                     'Content-Type': 'application/json'})

        self.assertEqual(response.status_code, 201)
        output = json.loads(response.get_data(as_text=True))
        self.assertEqual('Item added successfully', output['message'])

    def test_update_item(self):
        item1 = {'name': 'Rafting'}
        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps(item1),
                                   headers={"Authorization":
                                            self.retrieve_token(),
                                            'Content-Type':
                                            'application/json'})
        self.assertEqual(response.status_code, 200)

    def test_delete_bucketlist(self):
        response = self.client.delete("/bucketlists/1/items/2",
                                      headers={"Authorization":
                                               self.retrieve_token(),
                                               'Content-Type':
                                               'application/json'})
        self.assertEqual(response.status_code, 204)
