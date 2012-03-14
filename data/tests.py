"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data.models import User, Category, Item

class UserTest(TestCase):
    USERNAME = 'asdf1234'
    FIRST_NAME = 'Asdf'
    LAST_NAME = 'Qwerty'
    EMAIL = 'asdf1234@mit.edu'
    PHONE = '(123)456-7890'

    def setUp(self):
        # create a user
        self.user = User.create_user(self.USERNAME, self.FIRST_NAME, \
                self.LAST_NAME, self.EMAIL, self.PHONE)

    def tearDown(self):
        # delete the user
        User.delete_user(self.user)

    def test_user(self):
        '''
        Tests to make sure that users can be queried
        and that their attributes are correct.
        '''
        # create a user

        # find the user and check it
        u = User.get_user(self.USERNAME)
        self.assertEqual(u, self.user)
        self.assertEqual(u.username, self.USERNAME)
        self.assertEqual(u.first_name, self.FIRST_NAME)
        self.assertEqual(u.last_name, self.LAST_NAME)
        self.assertEqual(u.email, self.EMAIL)
        self.assertEqual(u.cell_phone, self.PHONE)

class CategoryTest(TestCase):
    CATEGORY_NAME = '3.091'

    def setUp(self):
        # create a category
        self.category = Category.create_category(self.CATEGORY_NAME)

    def tearDown(self):
        # delete the category
        Category.delete_category(self.category)

    def test_categories(self):
        '''
        Tests to make sure that categories can be queried
        and that the attributes are correct.
        '''
        # find the category and check it
        c = Category.get_category(self.CATEGORY_NAME)
        self.assertEqual(c, self.category)
        self.assertEqual(c.name, self.CATEGORY_NAME)

class ItemTest(TestCase):
    USERNAME = 'asdf1234'
    FIRST_NAME = 'Asdf'
    LAST_NAME = 'Qwerty'
    EMAIL = 'asdf1234@mit.edu'
    PHONE = '(123)456-7890'

    TEXTBOOK_CATEGORY = '3.091'
    VIDEOS_CATEGORY = '5.111'

    TEXTBOOK_NAME = '3.091 Textbook'
    TEXTBOOK_DESCRIPTION = 'The textbook for the legendary class ... 3.091!'
    VIDEOS_NAME = '5.111 Video Lecture Series'
    VIDEOS_DESCRIPTION = 'Watch 5-fun-fun-fun!'

    def setUp(self):
        # create the user
        self.user = User.create_user(self.USERNAME, self.FIRST_NAME, \
                self.LAST_NAME, self.EMAIL, self.PHONE)

        # create the categories
        self.category1 = Category.create_category(self.TEXTBOOK_CATEGORY)
        self.category2 = Category.create_category(self.VIDEOS_CATEGORY)

        # create the items
        self.item1 = Item.create_item(self.user, self.TEXTBOOK_NAME, \
                self.TEXTBOOK_DESCRIPTION, self.category1)
        self.item2 = self.user.add_item(self.TEXTBOOK_NAME, \
                self.TEXTBOOK_DESCRIPTION, self.category1)
        self.item3 = self.user.add_item(self.VIDEOS_NAME, \
                self.VIDEOS_DESCRIPTION, self.category2)

    def tearDown(self):
        # delete the items
        Item.delete_item(self.item1)
        Item.delete_item(self.item2)
        Item.delete_item(self.item3)

        # delete the categories
        Category.delete_category(self.category1)
        Category.delete_category(self.category2)

        # delete the user
        User.delete_user(self.user)

    def test_items(self):
        # check to make sure that both ways of getting items work
        for items in [Item.get_items(self.user), self.user.get_items()]:
            # check the item count
            self.assertEqual(len(items), 3)

            self.assertTrue(self.item1 in items)
            self.assertTrue(self.item2 in items)
            self.assertTrue(self.item3 in items)

