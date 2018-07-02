import unittest
from api.modals.user import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.test_user = User(1, 'name', 'example@mail.com', '12345', '12345')
        
    def test_authentication_encoding(self):
        auth_token = self.test_user.encode_authentication_token(self.test_user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        
    def test_authentication_decoding(self):
        auth_token = self.test_user.encode_authentication_token(self.test_user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertEqual(User.decode_authentication_token(auth_token), 1)


if __name__ == "__main__":
    unittest.main()
