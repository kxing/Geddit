"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data.models import User, Category

class UserTest(TestCase):
    def setUp(self):
        # create a user
        User.create_user('asdf1234', 'Asdf', 'Qwerty', 'asdf1234@mit.edu', '(123)456-7890')

    def tearDown(self):
        u = User.objects.get(username='asdf1234')

        # delete the user
        User.delete_user(u)

    def test_user(self):
        """
        Tests to make sure that users can be queried, and that their attributes are correct.
        """
        # create a user

        # find the user and check it
        u = User.get_user('asdf1234')
        self.assertEqual(u.username, 'asdf1234')
        self.assertEqual(u.first_name, 'Asdf')
        self.assertEqual(u.last_name, 'Qwerty')
        self.assertEqual(u.email, 'asdf1234@mit.edu')
        self.assertEqual(u.cell_phone, '(123)456-7890')

'''
class CategoryTest(TestCase):
    def test_categories(self):
        self.assertEqual
'''
