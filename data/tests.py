"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data.models import User

class UserTest(TestCase):
    def test_users(self):
        """
        Tests to make sure that users can be created, deleted, and queried.
        """
        # create a user
        User.create_user('asdf1234', 'Asdf', 'Qwerty', 'asdf1234@mit.edu')

        # find the user and check it
        u = User.get_user('asdf1234')
        self.assertEqual(u.username, 'asdf1234')
        self.assertEqual(u.first_name, 'Asdf')
        self.assertEqual(u.last_name, 'Qwerty')
        self.assertEqual(u.email, 'asdf1234@mit.edu')

        # delete the user
        User.delete_user(u)

        # check that the user isn't there anymore
        self.assertRaises(User.DoesNotExist, User.get_user, 'kxing')

