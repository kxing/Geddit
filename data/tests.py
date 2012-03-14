"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from data.models import User, Category, Item

class UserTest(TestCase):
    def setUp(self):
        # create a user
        self.user = User.create_user('asdf1234', 'Asdf', 'Qwerty', \
                'asdf1234@mit.edu', '(123)456-7890')

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
        u = User.get_user('asdf1234')
        self.assertEqual(u, self.user)
        self.assertEqual(u.username, 'asdf1234')
        self.assertEqual(u.first_name, 'Asdf')
        self.assertEqual(u.last_name, 'Qwerty')
        self.assertEqual(u.email, 'asdf1234@mit.edu')
        self.assertEqual(u.cell_phone, '(123)456-7890')

class CategoryTest(TestCase):
    def setUp(self):
        # create a category
        self.category = Category.create_category('3.091')

    def tearDown(self):
        # delete the category
        Category.delete_category(self.category)

    def test_categories(self):
        '''
        Tests to make sure that categories can be queried
        and that the attributes are correct.
        '''
        # find the category and check it
        c = Category.get_category('3.091')
        self.assertEqual(c, self.category)
        self.assertEqual(c.name, '3.091')

class ItemTest(TestCase):
    TEXTBOOK_NAME = '3.091 Textbook'
    TEXTBOOK_DESCRIPTION = 'The textbook for the legendary class ... 3.091!'
    VIDEOS_NAME = '5.111 Video Lecture Series'
    VIDEOS_DESCRIPTION = 'Watch 5-fun-fun-fun!'

    def setUp(self):
        # create the user
        self.user = User.create_user('asdf1234', 'Asdf', 'Qwerty', \
                'asdf1234@mit.edu', '(123)456-7890')

        # create the categories
        self.category1 = Category.create_category('3.091')
        self.category2 = Category.create_category('5.111')

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
        for items in [Item.get_items(self.user), self.user.get_items()]:
            self.assertEqual(len(items), 3)

            textbooks = []
            videos = []

            for item in items:
                if item.seller_user == self.user and \
                        item.name == self.TEXTBOOK_NAME and \
                        item.description == self.TEXTBOOK_DESCRIPTION and \
                        item.active and \
                        item.category == self.category1:
                    textbooks.append(item)
                elif item.seller_user == self.user and \
                        item.name == self.VIDEOS_NAME and \
                        item.description == self.VIDEOS_DESCRIPTION and \
                        item.active and \
                        item.category == self.category2:
                    videos.append(item)

            self.assertEqual(len(textbooks), 2)
            self.assertNotEqual(textbooks[0], textbooks[1])
            self.assertEqual(len(videos), 1)
