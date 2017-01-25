from tests.test import BaseTest
import json


class TestItem(BaseTest):
    def test_add_item(self):
        item3 = {'name': 'Zip Lining'}
        response = self.client.post(
            '/bucketlists/1/items/',
            data=json.dumps(item3), headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        message = json.loads(response.data)
        self.assertIn(message, 'Item added Successfully')

    def test_get_items(self):

        response = self.client.get(
            '/bucketlists/1/items', headers=self.get_token)
        self.assertEqual(response.status_code, 200)

    def test_get_item_with_id(self):
        item4 = {'name': 'Hot Air Balloon'}
        self.client.post(
            '/bucketlists/1/items/',
            data=json.dumps(item4), headers=self.get_token())
        response = self.client.get(
            '/bucketlists/1/items/4', headers=self.get_token)
        self.assertEqual(response.status_code, 200)
        item4 = json.loads(response.data)
        self.assertEqual(item4.get('name'), 'Hot Air Balloon')

    def test_get_item_with_nonexistent_id(self):

        response = self.client.get("/bucketlists/1/items/7",
                                   headers=self.get_token())
        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data)
        self.assertEqual(output['message'], 'Item does not exist')

    def test_update_item(self):
        item4 = {'name': 'Rafting', 'done': 'True'}
        response = self.client.put("/bucketlists/1/items/4",
                                   data=item4,
                                   headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertIn(output['message'],
                      'Item updated successfully')
        self.assertEqual(item4.get['name'], 'Rafting')

    def test_delete_bucketlist(self):
        response = self.client.delete("/bucketlists/1/items/2",
                                      data=self.bucketlist1,
                                      headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data)
        self.assertIn(output['message'],
                      'item deleted successfully')
# test search item with name
