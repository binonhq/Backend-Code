from cgitb import text
from email import header
from email.quoprimime import header_check
from urllib import request, response
from wsgiref import headers
import pymongo

from app.utils.jwt_utils import generate_jwt
from main import app
import json
import unittest
from app.models.book import Book
from app.models.user import User
from app.databases.mongodb import MongoDB

_db = MongoDB()

class UsersTest(unittest.TestCase):
    """ Unit testcases for REST APIs """

    def test_get_all_users(self):
        request, response = app.test_client.get('/users')
        self.assertEqual(response.status, 200)
        data = json.loads(response.text)
        self.assertGreaterEqual(data.get('n_users'), 0)
        self.assertIsInstance(data.get('users'), list)
        
    def test_register_users(self):
        key_register = json.dumps({
            "username" : "test",
            "password" : "test"
        })
        request_register, response_register = app.test_client.post('/users/register',
                                                             data=key_register)

        self.assertEqual(response_register.status, 200)
        self.assertEqual(json.loads(response_register.text).get("status"),"User create success")

    def 
    # def test_get_book_by_ID(self):
    #     latest_book =_db._books_col.find_one({}, sort=[('createdAt', pymongo.ASCENDING)])
    #     book_id = latest_book.get("_id")
    #     # Get with wrong ID - Check
    #     request_noId, response_noId = app.test_client.get('/books/noID')
    #     status_noId = 400
    #     self.assertEqual(response_noId.status, status_noId)
    #     # Get with true ID - Check
    #     request_Id, response_Id = app.test_client.get(
    #         f'/books/{book_id}')
    #     status_Id = 200
    #     self.assertEqual(response_Id.status, status_Id)

    # def test_update_book(self):
    #     latest_book =_db._books_col.find_one(sort = [('createdAt', pymongo.DESCENDING)])
    #     book_id = latest_book.get("_id")
    #     key_update_book = json.dumps({
    #         "title": "Book Test - Update",
    #     })
    #     # Update without register - Check
    #     header = {
    #         'Authorization': ""
    #     }
    #     request_noregister, response_noregister = app.test_client.put(
    #         f'/books/{book_id}', data=key_update_book, headers=header)
    #     status_noregister = 401
    #     self.assertEqual(response_noregister.status, status_noregister)
    #     self.assertEqual(json.loads(response_noregister.text).get(
    #         'message'), "Unauthorized: No one was register")

    #     # Update with owner - Check
    #     key_register = json.dumps({
    #         "username": "admin",
    #         "password": "admin"
    #     })
    #     request_register, response_register = app.test_client.post(
    #         '/users/register', data=key_register)
    #     jwt_code = json.loads(response_register.text).get('user').get('jwt_token')
    #     header = {
    #         'Authorization': jwt_code
    #     }
    #     request_update_book, response_update_book = app.test_client.put(f'/books/{book_id}',
    #                                                                     data=key_update_book,
    #                                                                     headers=header
    #                                                                     )
    #     self.assertEqual(response_update_book.status, 200)

    #     # Update with wrong ID - Check
    #     request_noId, response_noId = app.test_client.put('/books/noID',
    #                                                       data=key_update_book,
    #                                                       headers=header)
    #     self.assertEqual(response_noId.status, 404)

    #     # Update with non-owner - Check
    #     request_non_owner_update_book, response_non_owner_update_book = app.test_client.put('/books/31bbe961-491a-4aa2-b9b2-d01c107bdc22',
    #                                                                                         data=key_update_book,
    #                                                                                         headers=header
    #                                                                                         )
    #     self.assertEqual(response_non_owner_update_book.status, 401)
    #     self.assertEqual(json.loads(response_non_owner_update_book.text).get(
    #         'message'), "Unauthorized: Dont have permission to update this book")
     
    # def test_delete_book(self):
    #     latest_book =_db._books_col.find_one(sort = [('createdAt', pymongo.DESCENDING)])
    #     book_id = latest_book.get("_id")
    #     # Delete without register - Check
    #     header = {
    #         'Authorization': ""
    #     }
    #     request_noregister, response_noregister = app.test_client.delete(
    #         f'/books/{book_id}',headers=header)
    #     status_noregister = 401
    #     self.assertEqual(response_noregister.status, status_noregister)
    #     # self.assertEqual(json.loads(response_noregister.text).get(
    #     #     'message'), "Unauthorized: No one was register")
        
    #     # Delete with non-owner - Check
    #     request_non_owner_delete_book, response_non_owner_delete_book = app.test_client.delete('/books/31bbe961-491a-4aa2-b9b2-d01c107bdc22',
    #                                                                                         headers=header
    #                                                                                         )
    #     self.assertEqual(response_non_owner_delete_book.status, 401)
    #     # self.assertEqual(json.loads(response_non_owner_delete_book.text).get(
    #     #     'message'), "Unauthorized: Dont have permission to delete this book")    
        
    #     # Delete with owner - Check
    #     key_register = json.dumps({
    #         "username": "admin",
    #         "password": "admin"
    #     })
    #     request_register, response_register = app.test_client.post(
    #         '/users/register', data=key_register)
    #     jwt_code = json.loads(response_register.text).get('user').get('jwt_token')
    #     header = {
    #         'Authorization': jwt_code
    #     }
    #     request_delete_book, response_delete_book = app.test_client.delete(f'/books/{book_id}',
    #                                                                     headers=header
    #                                                                     )
    #     self.assertEqual(response_delete_book.status, 200)

    #     # Delete with wrong ID - Check
    #     request_noId, response_noId = app.test_client.delete('/books/noID',
    #                                                       headers=header)
    #     self.assertEqual(response_noId.status, 404)


    # TODO: unittest for another apis
if __name__ == '__main__':
    unittest.main()
